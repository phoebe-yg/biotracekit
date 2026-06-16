from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


ENTRYPOINT_NAMES = {"main.nf", "Snakefile", "workflow.cwl"}
CONFIG_SUFFIXES = {".config", ".yaml", ".yml", ".json", ".toml"}
OUTPUT_DIR_NAMES = {"results", "result", "outputs", "output", "out"}
IGNORED_DIRS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "dossier"}
TEXT_SUFFIXES = {".cwl", ".config", ".csv", ".json", ".md", ".nf", ".py", ".sh", ".smk", ".toml", ".tsv", ".txt", ".yaml", ".yml"}

CONTAINER_PATTERNS = [
    re.compile(r"\bcontainer\s+['\"]([^'\"]+)['\"]"),
    re.compile(r"\b(?:docker|singularity|apptainer)://[^\s'\"),]+"),
    re.compile(r"\b(?:quay\.io|ghcr\.io|docker\.io|biocontainers)/[^\s'\"),]+"),
]
NEXTFLOW_PROCESS_PATTERN = re.compile(r"\bprocess\s+([A-Za-z0-9_]+)")
PARAM_PATTERN = re.compile(r"\bparams\.([A-Za-z0-9_.-]+)\s*=\s*([^\n#]+)")


@dataclass(frozen=True)
class Check:
    key: str
    label: str
    passed: bool
    gap: str


def scan_workflow(path: Path) -> dict:
    root = path.resolve()
    if not root.exists():
        raise FileNotFoundError(f"Scan path does not exist: {path}")
    if not root.is_dir():
        raise NotADirectoryError(f"Scan path must be a directory: {path}")

    all_files = sorted(_iter_files(root), key=lambda item: item.as_posix())
    rel_files = [_relative(file, root) for file in all_files]
    text_by_file = {file: _read_text(file) for file in all_files if file.suffix in TEXT_SUFFIXES}

    entrypoints = _find_entrypoints(all_files, root)
    sample_sheets = _find_sample_sheets(all_files, root)
    configs = _find_configs(all_files, root)
    outputs = _find_outputs(root)
    containers = _find_containers(text_by_file)
    tools = _find_tool_hints(text_by_file)
    parameters = _find_parameters(text_by_file)
    engine = _detect_engine(entrypoints, rel_files)

    checks = _build_checks(
        entrypoints=entrypoints,
        sample_sheets=sample_sheets,
        configs=configs,
        outputs=outputs,
        containers=containers,
        rel_files=rel_files,
    )
    passed = sum(1 for check in checks if check.passed)
    total = len(checks)
    gaps = [check.gap for check in checks if not check.passed]

    return {
        "schema_version": "0.1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": {
            "path": str(root),
            "file_count": len(rel_files),
        },
        "workflow": {
            "engine": engine,
            "entrypoints": entrypoints,
        },
        "score": {
            "passed": passed,
            "total": total,
            "percent": round((passed / total) * 100),
        },
        "checks": [
            {
                "key": check.key,
                "label": check.label,
                "passed": check.passed,
            }
            for check in checks
        ],
        "files": {
            "entrypoints": entrypoints,
            "sample_sheets": sample_sheets,
            "configs": configs,
            "outputs": outputs,
            "all": rel_files,
        },
        "containers": containers,
        "tools": tools,
        "parameters": parameters,
        "gaps": gaps,
    }


def _iter_files(root: Path) -> Iterable[Path]:
    for item in root.rglob("*"):
        if any(part in IGNORED_DIRS for part in item.parts):
            continue
        if item.is_file():
            yield item


def _relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ""


def _find_entrypoints(files: list[Path], root: Path) -> list[str]:
    entries = []
    for file in files:
        if file.name in ENTRYPOINT_NAMES or file.suffix == ".cwl" or file.suffix == ".ga":
            entries.append(_relative(file, root))
    return sorted(set(entries))


def _find_sample_sheets(files: list[Path], root: Path) -> list[str]:
    sheets = []
    for file in files:
        lower_name = file.name.lower()
        if file.suffix.lower() not in {".csv", ".tsv"}:
            continue
        if any(token in lower_name for token in ("sample", "samples", "metadata", "manifest")):
            if _looks_like_table(file):
                sheets.append(_relative(file, root))
    return sorted(set(sheets))


def _looks_like_table(path: Path) -> bool:
    delimiter = "\t" if path.suffix.lower() == ".tsv" else ","
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.reader(handle, delimiter=delimiter))
    except UnicodeDecodeError:
        return False
    return len(rows) >= 2 and len(rows[0]) >= 2


def _find_configs(files: list[Path], root: Path) -> list[str]:
    configs = []
    for file in files:
        lower_name = file.name.lower()
        if file.suffix.lower() in CONFIG_SUFFIXES or lower_name in {"nextflow.config", "params.json"}:
            configs.append(_relative(file, root))
    return sorted(set(configs))


def _find_outputs(root: Path) -> list[str]:
    outputs = []
    for item in root.iterdir():
        if item.is_dir() and item.name.lower() in OUTPUT_DIR_NAMES:
            outputs.append(item.name + "/")
    return sorted(set(outputs))


def _find_containers(text_by_file: dict[Path, str]) -> list[str]:
    containers: set[str] = set()
    for text in text_by_file.values():
        for pattern in CONTAINER_PATTERNS:
            for match in pattern.finditer(text):
                if match.groups():
                    containers.add(match.group(1).strip())
                else:
                    containers.add(match.group(0).strip())
    return sorted(containers)


def _find_tool_hints(text_by_file: dict[Path, str]) -> list[str]:
    tools: set[str] = set()
    for text in text_by_file.values():
        for match in NEXTFLOW_PROCESS_PATTERN.finditer(text):
            tools.add(match.group(1))
    return sorted(tools)


def _find_parameters(text_by_file: dict[Path, str]) -> dict[str, str]:
    params = {}
    for text in text_by_file.values():
        for match in PARAM_PATTERN.finditer(text):
            params[match.group(1)] = match.group(2).strip().strip("'\"")
    return dict(sorted(params.items()))


def _detect_engine(entrypoints: list[str], rel_files: list[str]) -> str:
    names = {Path(file).name for file in entrypoints + rel_files}
    if "main.nf" in names or "nextflow.config" in names:
        return "nextflow"
    if "Snakefile" in names:
        return "snakemake"
    if any(file.endswith(".cwl") for file in rel_files):
        return "cwl"
    if any(file.endswith(".ga") for file in rel_files):
        return "galaxy"
    return "unknown"


def _build_checks(
    *,
    entrypoints: list[str],
    sample_sheets: list[str],
    configs: list[str],
    outputs: list[str],
    containers: list[str],
    rel_files: list[str],
) -> list[Check]:
    names = {Path(file).name.lower() for file in rel_files}
    return [
        Check("entrypoint", "Workflow entry point detected", bool(entrypoints), "Add a workflow entry point such as main.nf, Snakefile, workflow.cwl, or a Galaxy .ga file."),
        Check("sample_sheet", "Sample sheet or metadata table detected", bool(sample_sheets), "Add a sample sheet or metadata table with at least two columns and one data row."),
        Check("config", "Configuration file detected", bool(configs), "Add a versioned config file that captures workflow parameters."),
        Check("container", "Container reference detected", bool(containers), "Add Docker, Singularity, Apptainer, or registry references for tool environments."),
        Check("readme", "README detected", "readme.md" in names or "readme" in names, "Add a README explaining the biological question and workflow usage."),
        Check("license", "License detected", "license" in names or "license.md" in names or "copying" in names, "Add a license so downstream users know how the workflow can be reused."),
        Check("outputs", "Output directory detected", bool(outputs), "Add or document an output directory such as results/ or outputs/."),
    ]
