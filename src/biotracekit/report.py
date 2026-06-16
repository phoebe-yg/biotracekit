from __future__ import annotations


def render_methods_markdown(dossier: dict) -> str:
    workflow = dossier["workflow"]
    files = dossier["files"]
    score = dossier["score"]

    lines = [
        "# BioTraceKit Methods Summary",
        "",
        f"Source: `{dossier['source']['path']}`",
        f"Workflow engine: `{workflow['engine']}`",
        f"FAIR readiness: **{score['percent']}%** ({score['passed']}/{score['total']} checks)",
        "",
        "## Entry Points",
    ]

    lines.extend(_bullet_list(files["entrypoints"]))
    lines.extend(["", "## Inputs and Sample Sheets"])
    lines.extend(_bullet_list(files["sample_sheets"]))
    lines.extend(["", "## Configuration"])
    lines.extend(_bullet_list(files["configs"]))
    lines.extend(["", "## Containers"])
    lines.extend(_bullet_list(dossier["containers"]))
    lines.extend(["", "## Tool Hints"])
    lines.extend(_bullet_list(dossier["tools"]))
    lines.extend(["", "## Parameters"])

    params = dossier["parameters"]
    if params:
        for key, value in params.items():
            lines.append(f"- `{key}`: `{value}`")
    else:
        lines.append("- None detected")

    lines.extend(["", "## Outputs"])
    lines.extend(_bullet_list(files["outputs"]))
    lines.extend(["", "## Reproducibility Gaps"])
    lines.extend(_bullet_list(dossier["gaps"]))
    lines.append("")

    return "\n".join(lines)


def _bullet_list(values: list[str]) -> list[str]:
    if not values:
        return ["- None detected"]
    return [f"- `{value}`" for value in values]
