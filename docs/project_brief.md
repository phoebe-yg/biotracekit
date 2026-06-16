# BioTraceKit Project Brief

## Problem

Computational biology workflows are increasingly central research artifacts, but the information needed to evaluate and reproduce a result is often split across scripts, workflow configs, container tags, sample sheets, command logs, manuscripts, and informal lab notes.

Workflow engines solve execution. They do not always solve the smaller but painful collaboration problem: "Can another scientist quickly understand what ran, with which data, tools, versions, parameters, and outputs?"

## Product

BioTraceKit is a workflow handoff assistant for computational biology. It scans a workflow repo or completed run directory and creates a reproducibility dossier that is useful before publication, before a lab handoff, and during internal review.

The dossier should include:

- Workflow engine and entry point.
- Inputs, sample sheets, reference data, and external accessions when discoverable.
- Tool and container inventory.
- Parameters and config files.
- Output files and quality-control artifacts.
- Metadata gaps that block reuse.
- Export formats for humans and machines.

## Users

- Computational biologists preparing analyses for publication.
- Bioinformatics core teams handing results to collaborators.
- Wet-lab scientists reviewing a completed sequencing analysis.
- Methods reviewers and maintainers checking reproducibility before release.
- Open source pipeline authors who want an adoption-friendly quality gate.

## Differentiation

BioTraceKit is not another workflow engine. It is a thin product layer around existing engines and standards:

- It can start with static scanning before requiring deep execution integration.
- It makes missing metadata visible early.
- It produces reviewer-friendly summaries, not just raw provenance.
- It can evolve toward RO-Crate, BioCompute Object, WorkflowHub, and engine-specific integrations.

## First Product Bet

The strongest wedge is a local CLI that developers can run in a workflow repository:

```bash
biotracekit scan examples/rnaseq --out dossier/
```

That command should produce:

- `dossier/biotracekit.json`
- `dossier/METHODS.md`
- a concise terminal scorecard

The second wedge is a static dashboard that opens the same dossier and makes it inspectable by non-developers.

## Non-Goals

- Replacing Nextflow, Snakemake, CWL, Galaxy, nf-core, or WorkflowHub.
- Claiming full regulatory BioCompute compliance in the first MVP.
- Uploading biological data by default.
- Running expensive analyses in the first product iteration.

## Success Metrics

- A user can scan a small workflow folder in under 10 seconds.
- The generated `METHODS.md` is useful enough to paste into a lab handoff draft.
- The JSON dossier can be validated by automated tests.
- The dashboard makes missing reproducibility information obvious without reading source code.
- Early adopters can add support for a new workflow engine by contributing one parser module.
