from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from biotracekit.report import render_methods_markdown
from biotracekit.scanner import scan_workflow


FIXTURE = Path(__file__).resolve().parents[1] / "examples" / "rnaseq"


class ScannerTests(TestCase):
    def test_scans_example_nextflow_workflow(self) -> None:
        dossier = scan_workflow(FIXTURE)

        self.assertEqual(dossier["workflow"]["engine"], "nextflow")
        self.assertEqual(dossier["score"]["percent"], 100)
        self.assertIn("main.nf", dossier["files"]["entrypoints"])
        self.assertIn("samples.tsv", dossier["files"]["sample_sheets"])
        self.assertIn("FASTQC", dossier["tools"])
        self.assertIn("MULTIQC", dossier["tools"])
        self.assertIn("quay.io/biocontainers/fastqc:0.12.1--hdfd78af_0", dossier["containers"])
        self.assertEqual(dossier["gaps"], [])

    def test_reports_gaps_for_sparse_folder(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "main.nf").write_text("process ALIGN {}\n", encoding="utf-8")

            dossier = scan_workflow(root)

        self.assertEqual(dossier["workflow"]["engine"], "nextflow")
        self.assertLess(dossier["score"]["percent"], 100)
        self.assertIn("Add a README explaining the biological question and workflow usage.", dossier["gaps"])

    def test_methods_markdown_includes_reviewer_sections(self) -> None:
        markdown = render_methods_markdown(scan_workflow(FIXTURE))

        self.assertIn("# BioTraceKit Methods Summary", markdown)
        self.assertIn("## Reproducibility Gaps", markdown)
        self.assertIn("FAIR readiness: **100%**", markdown)
