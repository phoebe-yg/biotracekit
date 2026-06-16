const sampleDossier = {
  schema_version: "0.1.0",
  generated_at: "2026-06-16T00:00:00+00:00",
  source: {
    path: "/lab/workflows/rnaseq",
    file_count: 7
  },
  workflow: {
    engine: "nextflow",
    entrypoints: ["main.nf"]
  },
  score: {
    passed: 6,
    total: 7,
    percent: 86
  },
  checks: [
    { key: "entrypoint", label: "Workflow entry point detected", passed: true },
    { key: "sample_sheet", label: "Sample sheet or metadata table detected", passed: true },
    { key: "config", label: "Configuration file detected", passed: true },
    { key: "container", label: "Container reference detected", passed: true },
    { key: "readme", label: "README detected", passed: true },
    { key: "license", label: "License detected", passed: false },
    { key: "outputs", label: "Output directory detected", passed: true }
  ],
  files: {
    entrypoints: ["main.nf"],
    sample_sheets: ["samples.tsv"],
    configs: ["nextflow.config"],
    outputs: ["results/"],
    all: ["README.md", "main.nf", "nextflow.config", "samples.tsv", "results/multiqc_report.html"]
  },
  containers: [
    "quay.io/biocontainers/fastqc:0.12.1--hdfd78af_0",
    "quay.io/biocontainers/multiqc:1.22.3--pyhdfd78af_0"
  ],
  tools: ["FASTQC", "MULTIQC"],
  parameters: {
    reads: "data/*.fastq.gz",
    genome: "GRCh38",
    outdir: "results"
  },
  gaps: [
    "Add a license so downstream users know how the workflow can be reused."
  ]
};

const state = {
  dossier: sampleDossier
};

const elements = {
  fileInput: document.getElementById("dossier-file"),
  resetSample: document.getElementById("reset-sample"),
  copyMethods: document.getElementById("copy-methods"),
  scoreRing: document.getElementById("score-ring"),
  scorePercent: document.getElementById("score-percent"),
  workflowEngine: document.getElementById("workflow-engine"),
  sourcePath: document.getElementById("source-path"),
  checkCount: document.getElementById("check-count"),
  fileCount: document.getElementById("file-count"),
  gapCount: document.getElementById("gap-count"),
  checksList: document.getElementById("checks-list"),
  entrypoints: document.getElementById("entrypoints"),
  sampleSheets: document.getElementById("sample-sheets"),
  outputs: document.getElementById("outputs"),
  mapInputs: document.getElementById("map-inputs"),
  mapWorkflow: document.getElementById("map-workflow"),
  mapOutputs: document.getElementById("map-outputs"),
  inventoryTable: document.getElementById("inventory-table"),
  gapsList: document.getElementById("gaps-list"),
  methodsSummary: document.getElementById("methods-summary")
};

function render(dossier) {
  state.dossier = normalizeDossier(dossier);
  const active = state.dossier;
  const score = active.score.percent || 0;

  elements.scoreRing.style.setProperty("--score", score);
  elements.scorePercent.textContent = `${score}%`;
  elements.workflowEngine.textContent = active.workflow.engine || "unknown";
  elements.sourcePath.textContent = active.source.path || "";
  elements.checkCount.textContent = `${active.score.passed}/${active.score.total}`;
  elements.fileCount.textContent = String(active.source.file_count || active.files.all.length);
  elements.gapCount.textContent = String(active.gaps.length);

  elements.checksList.replaceChildren(...active.checks.map(renderCheck));
  elements.entrypoints.textContent = formatList(active.files.entrypoints);
  elements.sampleSheets.textContent = formatList(active.files.sample_sheets);
  elements.outputs.textContent = formatList(active.files.outputs);
  elements.mapInputs.textContent = active.files.sample_sheets.length ? active.files.sample_sheets[0] : "Inputs";
  elements.mapWorkflow.textContent = active.workflow.engine || "Workflow";
  elements.mapOutputs.textContent = active.files.outputs.length ? active.files.outputs[0] : "Outputs";

  elements.inventoryTable.replaceChildren(...renderInventory(active));
  renderGaps(active.gaps);
  elements.methodsSummary.textContent = renderMethods(active);
}

function normalizeDossier(dossier) {
  const files = dossier.files || {};
  const score = dossier.score || {};
  const checks = Array.isArray(dossier.checks) ? dossier.checks : [];
  const gaps = Array.isArray(dossier.gaps) ? dossier.gaps : [];
  const total = score.total || checks.length || 0;
  const passed = score.passed ?? checks.filter((check) => check.passed).length;
  const percent = score.percent ?? (total ? Math.round((passed / total) * 100) : 0);

  return {
    ...dossier,
    source: {
      path: dossier.source?.path || "",
      file_count: dossier.source?.file_count || (files.all || []).length
    },
    workflow: {
      engine: dossier.workflow?.engine || "unknown",
      entrypoints: dossier.workflow?.entrypoints || files.entrypoints || []
    },
    score: { passed, total, percent },
    checks,
    files: {
      entrypoints: files.entrypoints || [],
      sample_sheets: files.sample_sheets || [],
      configs: files.configs || [],
      outputs: files.outputs || [],
      all: files.all || []
    },
    containers: dossier.containers || [],
    tools: dossier.tools || [],
    parameters: dossier.parameters || {},
    gaps
  };
}

function renderCheck(check) {
  const row = document.createElement("div");
  row.className = `check-row ${check.passed ? "pass" : "fail"}`;

  const stateBadge = document.createElement("span");
  stateBadge.className = "check-state";
  stateBadge.textContent = check.passed ? "OK" : "!";

  const label = document.createElement("p");
  label.className = "check-label";
  label.textContent = check.label || check.key || "Unnamed check";

  row.append(stateBadge, label);
  return row;
}

function renderInventory(dossier) {
  const rows = [];
  rows.push(...dossier.tools.map((tool) => tableRow("Tool", tool)));
  rows.push(...dossier.containers.map((container) => tableRow("Container", container)));
  rows.push(...Object.entries(dossier.parameters).map(([key, value]) => tableRow(`Parameter: ${key}`, value)));

  if (!rows.length) {
    rows.push(tableRow("Inventory", "None detected"));
  }

  return rows;
}

function tableRow(type, value) {
  const row = document.createElement("tr");
  const typeCell = document.createElement("td");
  const valueCell = document.createElement("td");
  const pill = document.createElement("span");

  pill.className = "pill";
  pill.textContent = type;
  typeCell.append(pill);
  valueCell.textContent = value;
  row.append(typeCell, valueCell);
  return row;
}

function renderGaps(gaps) {
  if (!gaps.length) {
    const empty = document.createElement("div");
    empty.className = "empty-state";
    empty.textContent = "No open metadata gaps";
    elements.gapsList.replaceChildren(empty);
    return;
  }

  const items = gaps.map((gap) => {
    const item = document.createElement("li");
    item.textContent = gap;
    return item;
  });
  elements.gapsList.replaceChildren(...items);
}

function renderMethods(dossier) {
  const lines = [
    "# BioTraceKit Methods Summary",
    "",
    `Source: ${dossier.source.path || "unknown"}`,
    `Workflow engine: ${dossier.workflow.engine}`,
    `FAIR readiness: ${dossier.score.percent}% (${dossier.score.passed}/${dossier.score.total} checks)`,
    "",
    "Entry points:",
    ...toBullets(dossier.files.entrypoints),
    "",
    "Inputs and sample sheets:",
    ...toBullets(dossier.files.sample_sheets),
    "",
    "Configuration:",
    ...toBullets(dossier.files.configs),
    "",
    "Containers:",
    ...toBullets(dossier.containers),
    "",
    "Tool hints:",
    ...toBullets(dossier.tools),
    "",
    "Parameters:",
    ...toBullets(Object.entries(dossier.parameters).map(([key, value]) => `${key}: ${value}`)),
    "",
    "Outputs:",
    ...toBullets(dossier.files.outputs),
    "",
    "Reproducibility gaps:",
    ...toBullets(dossier.gaps)
  ];

  return lines.join("\n");
}

function toBullets(values) {
  return values.length ? values.map((value) => `- ${value}`) : ["- None detected"];
}

function formatList(values) {
  return values.length ? values.join(", ") : "None detected";
}

async function handleFileLoad(event) {
  const [file] = event.target.files;
  if (!file) {
    return;
  }

  const text = await file.text();
  render(JSON.parse(text));
}

async function copyMethods() {
  const text = elements.methodsSummary.textContent || "";
  let copied = false;

  if (await canWriteClipboard()) {
    try {
      await window.navigator.clipboard.writeText(text);
      copied = true;
    } catch (_error) {
      copied = false;
    }
  }

  if (!copied) {
    selectMethodsText();
  }

  elements.copyMethods.textContent = copied ? "Copied" : "Selected";
  window.setTimeout(() => {
    elements.copyMethods.textContent = "Copy Methods";
  }, 1400);
}

async function canWriteClipboard() {
  if (!window.navigator?.clipboard?.writeText || !window.navigator?.permissions?.query) {
    return false;
  }

  try {
    const permission = await window.navigator.permissions.query({ name: "clipboard-write" });
    return permission.state === "granted";
  } catch (_error) {
    return false;
  }
}

function selectMethodsText() {
  const selection = window.getSelection();
  const range = document.createRange();
  range.selectNodeContents(elements.methodsSummary);
  selection.removeAllRanges();
  selection.addRange(range);
}

elements.fileInput.addEventListener("change", handleFileLoad);
elements.resetSample.addEventListener("click", () => render(sampleDossier));
elements.copyMethods.addEventListener("click", copyMethods);

render(sampleDossier);
