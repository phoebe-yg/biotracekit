from __future__ import annotations

import argparse
import json
from pathlib import Path

from .report import render_methods_markdown
from .scanner import scan_workflow


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="biotracekit",
        description="Generate a reproducibility dossier for a computational biology workflow.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan = subparsers.add_parser("scan", help="Scan a workflow folder.")
    scan.add_argument("path", type=Path, help="Workflow repository or run directory to scan.")
    scan.add_argument(
        "--out",
        type=Path,
        default=Path("dossier"),
        help="Output directory for biotracekit.json and METHODS.md.",
    )
    scan.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON output.",
    )
    return parser


def run_scan(path: Path, out_dir: Path, pretty: bool = False) -> int:
    dossier = scan_workflow(path)
    out_dir.mkdir(parents=True, exist_ok=True)

    json_path = out_dir / "biotracekit.json"
    methods_path = out_dir / "METHODS.md"

    json_path.write_text(
        json.dumps(dossier, indent=2 if pretty else None, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    methods_path.write_text(render_methods_markdown(dossier), encoding="utf-8")

    score = dossier["score"]["percent"]
    passed = dossier["score"]["passed"]
    total = dossier["score"]["total"]
    engine = dossier["workflow"]["engine"]

    print(f"BioTraceKit dossier written to {out_dir}")
    print(f"Engine: {engine}")
    print(f"FAIR readiness: {score}% ({passed}/{total} checks)")

    if dossier["gaps"]:
        print("Top gaps:")
        for gap in dossier["gaps"][:3]:
            print(f"- {gap}")

    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "scan":
        return run_scan(args.path, args.out, args.pretty)

    parser.error(f"Unknown command: {args.command}")
    return 2
