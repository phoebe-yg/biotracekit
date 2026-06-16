# Research Notes

Research snapshot: 2026-06-16.

## Signals

- The Workflows Community Initiative argues that computational workflows are publishable research objects and should be made Findable, Accessible, Interoperable, and Reusable.
- Workflow Run RO-Crate provides a model for recording workflow execution provenance, including inputs, outputs, code, and related run objects.
- WorkflowHub frames workflow sharing as a way to reduce reinvention, improve method transparency, and make workflows easier to find across diverse engines.
- Nextflow, nf-core, Snakemake, CWL, and Galaxy show that workflow execution is a mature area, but documentation and handoff quality still vary across labs and projects.
- BioCompute Objects are relevant to high-throughput sequencing provenance, especially where regulated or clinical review matters.

## Sources

- Applying the FAIR Principles to Computational Workflows: https://arxiv.org/abs/2410.03490
- An Ecosystem of Services for FAIR Computational Workflows: https://arxiv.org/abs/2505.15988
- Recording provenance of workflow runs with RO-Crate: https://arxiv.org/abs/2312.07852
- WorkflowHub: a registry for computational workflows: https://arxiv.org/abs/2410.06941
- Supporting Workflow Reproducibility by Linking Bioinformatics Tools across Papers and Executable Code: https://arxiv.org/abs/2603.08195
- Galaxy platform background: https://galaxyproject.org/
- nf-core community pipelines: https://nf-co.re/
- BioCompute Object project: https://osf.io/h59uh/

## Opportunity

There is room for a developer-friendly, local-first product that helps teams improve metadata completeness before they publish or share results. The first version should not attempt full standard compliance. It should generate a pragmatic dossier, expose gaps, and make it easy to evolve toward formal exports.

## Product Principles

- Local first: do not require users to upload private genomic data.
- Standards-aware: align fields with RO-Crate and BioCompute concepts where practical.
- Human-readable by default: every machine artifact should have a reviewer-facing equivalent.
- Workflow-engine agnostic: start with simple static detectors and add deeper integrations over time.
- Extensible: parser modules should be small and testable.
