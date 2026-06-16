# MVP Plan

## Branch 1: `mvp/cli-dossier`

Goal: prove that a local scanner can create a useful dossier from a workflow folder.

Scope:

- Python package with a `biotracekit` CLI.
- Static scan for common workflow files: `nextflow.config`, `main.nf`, `Snakefile`, `workflow.cwl`, `samples.tsv`, `samples.csv`, and container references.
- FAIR readiness checks for entry point, sample sheet, container declaration, README, license, config, and output directory.
- JSON output with score, detected files, tool hints, and gaps.
- Markdown `METHODS.md` output for human review.
- Unit tests over a tiny example workflow.

Out of scope:

- Running workflows.
- Parsing every syntax edge case.
- Uploading to registries.

## Branch 2: `mvp/web-reviewer`

Goal: prove that a generated dossier can become a useful review surface for non-developer collaborators.

Scope:

- Static HTML/CSS/JS app.
- Loads a sample BioTraceKit dossier.
- Shows score, detected workflow engine, files, tool inventory, and missing metadata.
- Provides a copyable methods summary.
- No build tool required.

Out of scope:

- Authentication.
- Server-side persistence.
- Live workflow scanning.

## Validation Questions

- Does the CLI find enough signal from real workflow folders to be useful?
- Does the dashboard reduce the time needed to review a workflow handoff?
- Which export target should come next: RO-Crate, BioCompute Object, or WorkflowHub metadata?
- Are users more interested in pre-run checks, post-run provenance, or manuscript methods drafts?
