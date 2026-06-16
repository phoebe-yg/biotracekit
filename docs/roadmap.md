# Roadmap

## Phase 0: Prototype

- Build the CLI dossier generator.
- Build the static reviewer dashboard.
- Use example workflows and fixtures only.
- Keep dependencies minimal.

## Phase 1: Real Workflow Support

- Add parser modules for Nextflow and Snakemake.
- Detect Conda, Docker, Singularity/Apptainer, and container digest references.
- Support sample sheets with schema hints.
- Generate RO-Crate-inspired JSON-LD.
- Add GitHub Actions support for reproducibility checks on pull requests.

## Phase 2: Collaboration

- Add a web viewer that can be published with GitHub Pages.
- Provide comments and checklist export for lab handoffs.
- Add comparison between two dossier versions.
- Support badges for README files.

## Phase 3: Standards and Ecosystem

- Add formal RO-Crate export.
- Add BioCompute Object draft export for sequencing workflows.
- Add WorkflowHub metadata export.
- Add plugin APIs for workflow engines and institution-specific metadata rules.

## Phase 4: Sustainability

- Create contributor docs and governance.
- Publish example dossiers for common workflow types.
- Build a small adopter program with bioinformatics cores.
- Define a stable JSON schema and compatibility policy.
