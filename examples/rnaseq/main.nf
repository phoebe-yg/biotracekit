params.reads = "data/*.fastq.gz"
params.genome = "GRCh38"
params.outdir = "results"

process FASTQC {
  container "quay.io/biocontainers/fastqc:0.12.1--hdfd78af_0"

  input:
  path reads

  output:
  path "fastqc.html"

  script:
  """
  fastqc ${reads}
  """
}

process MULTIQC {
  container "quay.io/biocontainers/multiqc:1.22.3--pyhdfd78af_0"

  input:
  path reports

  output:
  path "multiqc_report.html"

  script:
  """
  multiqc .
  """
}
