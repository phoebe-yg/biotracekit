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

## Step-by-Step Usage Guide

### 1. Use the CLI dossier MVP

Check out the CLI branch:

```bash
git switch mvp/cli-dossier
```

Run the scanner against the included example RNA-seq workflow:

```bash
PYTHONPATH=src python3 -m biotracekit scan examples/rnaseq --out dossier --pretty
```

BioTraceKit writes two files:

- `dossier/biotracekit.json`: machine-readable workflow dossier.
- `dossier/METHODS.md`: human-readable methods summary.

Open `dossier/METHODS.md` first. It is the quickest way to review the detected workflow engine, entry points, sample sheets, containers, parameters, outputs, and reproducibility gaps.

### 2. Scan your own workflow folder

Run the same command against a local workflow repository or completed run folder:

```bash
PYTHONPATH=src python3 -m biotracekit scan /path/to/your/workflow --out dossier --pretty
```

The current prototype looks for:

- workflow entry points such as `main.nf`, `Snakefile`, `workflow.cwl`, and Galaxy `.ga` files.
- sample sheets such as `samples.tsv`, `samples.csv`, metadata tables, and manifests.
- config files such as `nextflow.config`, JSON, YAML, TOML, and related parameter files.
- container references from Docker, Singularity, Apptainer, `quay.io`, `ghcr.io`, `docker.io`, and BioContainers.
- output folders such as `results/`, `outputs/`, and `out/`.

### 3. Interpret the score

The terminal output shows a FAIR readiness score:

```text
FAIR readiness: 100% (7/7 checks)
```

Treat the score as an early review checklist, not as a formal compliance claim. A lower score means the folder is missing handoff metadata such as a README, license, sample sheet, config, container reference, or output directory.

### 4. Inspect the dossier in the web reviewer MVP

Check out the web branch:

```bash
git switch mvp/web-reviewer
```

Start a local static server:

```bash
python3 -m http.server 4173 --directory web
```

Open this URL:

```text
http://127.0.0.1:4173
```

The dashboard loads a sample dossier by default. Use `Load JSON` to select a generated `biotracekit.json` file from the CLI MVP.

### 5. Expected workflow

For day-to-day use, the intended flow is:

1. Run the CLI against a workflow folder.
2. Read the generated `METHODS.md`.
3. Fix any gaps BioTraceKit reports.
4. Share `biotracekit.json` with collaborators or load it into the reviewer dashboard.
5. Repeat before publication, handoff, or release.

## Documentation

- [Project brief](docs/project_brief.md)
- [Research notes](docs/research_notes.md)
- [MVP plan](docs/mvp_plan.md)
- [Roadmap](docs/roadmap.md)

## License

MIT
