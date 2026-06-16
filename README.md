# BioTraceKit

BioTraceKit is an open source product concept for computational biology teams that need to make workflow runs easier to inspect, reproduce, and share.

The product sits next to tools such as Nextflow, Snakemake, CWL, and Galaxy. It scans a workflow repository or completed run folder, detects reproducibility metadata, and produces a lightweight "run dossier" for collaborators, reviewers, and future lab members.

## Core Idea

Computational biology already has strong workflow engines, but many analyses still ship as scattered scripts, hidden parameter choices, incomplete environment notes, and hard-to-review output folders. BioTraceKit focuses on the handoff layer:

- A FAIR readiness score for a workflow or run folder.
- A machine-readable provenance bundle inspired by RO-Crate and BioCompute Objects.
- A human-readable methods summary for papers, lab notebooks, and pull requests.
- A dashboard that lets scientists inspect inputs, tools, containers, outputs, and missing metadata before publication.

## MVP Branches

This repository uses `main` for the product brief and planning docs. Two prototype branches explore different MVP directions:

- `mvp/cli-dossier`: a Python CLI that scans a small workflow folder and emits a JSON dossier plus a Markdown methods summary.
- `mvp/web-reviewer`: a static reviewer dashboard for inspecting a BioTraceKit dossier in the browser.

## Documentation

- [Project brief](docs/project_brief.md)
- [Research notes](docs/research_notes.md)
- [MVP plan](docs/mvp_plan.md)
- [Roadmap](docs/roadmap.md)

## License

MIT
