import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { MeTTa } from "../_vendor/MeTTaScript/packages/hyperon/dist/index.js";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");
const corpusPath = path.join(root, "certification", "differential-four-color-v1.json");
const outDir = path.join(root, "artifacts", "witnesses");
const outPath = path.join(outDir, "differential-execution.json");
const METTASCRIPT_COMMIT = "abe13439196bccdb48b6636773a46ec9772a7aaf";

function sha256(data) {
  return crypto.createHash("sha256").update(data).digest("hex");
}

function repoSha() {
  const result = spawnSync("git", ["rev-parse", "HEAD"], { cwd: root, encoding: "utf8" });
  if (result.status !== 0) throw new Error(`git rev-parse failed: ${result.stderr}`);
  return result.stdout.trim();
}

function normalizeGraph(graph) {
  const vertices = Object.keys(graph).sort();
  const normalized = {};
  for (const vertex of vertices) {
    normalized[vertex] = [...graph[vertex]].sort();
  }
  return normalized;
}

function validateGraph(graph) {
  const vertices = new Set(Object.keys(graph));
  for (const [vertex, neighbors] of Object.entries(graph)) {
    if (!Array.isArray(neighbors)) throw new Error(`${vertex}: neighbors must be an array`);
    if (new Set(neighbors).size !== neighbors.length) throw new Error(`${vertex}: duplicate neighbor`);
    if (neighbors.includes(vertex)) throw new Error(`${vertex}: self-loop is outside certified corpus`);
    for (const neighbor of neighbors) {
      if (!vertices.has(neighbor)) throw new Error(`${vertex}: unknown neighbor ${neighbor}`);
      if (!graph[neighbor].includes(vertex)) throw new Error(`${vertex}-${neighbor}: graph must be symmetric`);
    }
  }
}

function runPython(graph) {
  const source = [
    "import json, sys",
    "from examples.four_color.solver import color_graph",
    "graph = json.loads(sys.stdin.read())",
    "result = color_graph(graph)",
    "print(json.dumps(result, sort_keys=True))",
  ].join("; ");
  const result = spawnSync(process.env.PYTHON || "python", ["-c", source], {
    cwd: root,
    input: JSON.stringify(graph),
    encoding: "utf8",
  });
  if (result.status !== 0) {
    throw new Error(`Python source execution failed: ${result.stderr || result.stdout}`);
  }
  return JSON.parse(result.stdout);
}

function undirectedEdges(graph, vertices) {
  const index = new Map(vertices.map((vertex, i) => [vertex, i]));
  const edges = [];
  for (const vertex of vertices) {
    for (const neighbor of graph[vertex]) {
      if (index.get(vertex) < index.get(neighbor)) edges.push([vertex, neighbor]);
    }
  }
  return edges;
}

function mettaProgram(graph) {
  const vertices = Object.keys(graph).sort();
  const variables = new Map(vertices.map((vertex, i) => [vertex, `$c${i}`]));
  let expression = `(coloring ${vertices.map((v) => `(${v} ${variables.get(v)})`).join(" ")})`;

  const edges = undirectedEdges(graph, vertices).reverse();
  for (const [left, right] of edges) {
    expression = `(if (== ${variables.get(left)} ${variables.get(right)}) (superpose ()) ${expression})`;
  }
  for (const vertex of [...vertices].reverse()) {
    expression = `(let ${variables.get(vertex)} (superpose (red green blue yellow)) ${expression})`;
  }
  return `(= (solve) ${expression})\n!(solve)\n`;
}

function runMetta(graph) {
  const runtime = new MeTTa();
  const program = mettaProgram(graph);
  const groups = runtime.run(program);
  const rendered = groups.flat().map(String);
  return { program, rendered };
}

function parseColoring(rendered, vertices) {
  if (vertices.length === 0) return {};
  const coloring = {};
  const pair = /\(([A-Za-z0-9_-]+)\s+(red|green|blue|yellow)\)/g;
  for (const match of rendered.matchAll(pair)) coloring[match[1]] = match[2];
  return coloring;
}

function validColoring(graph, coloring) {
  const vertices = Object.keys(graph);
  if (Object.keys(coloring).length !== vertices.length) return false;
  for (const vertex of vertices) {
    if (!["red", "green", "blue", "yellow"].includes(coloring[vertex])) return false;
    for (const neighbor of graph[vertex]) {
      if (coloring[vertex] === coloring[neighbor]) return false;
    }
  }
  return true;
}

const corpusBytes = fs.readFileSync(corpusPath);
const corpus = JSON.parse(corpusBytes);
if (corpus.schema !== "mettafy-differential-four-color-v1") {
  throw new Error(`unsupported corpus schema ${corpus.schema}`);
}
if (!Array.isArray(corpus.cases) || corpus.cases.length === 0) throw new Error("empty corpus");

const seen = new Set();
const cases = [];
let mismatchCount = 0;
for (const testCase of corpus.cases) {
  if (seen.has(testCase.id)) throw new Error(`duplicate case id ${testCase.id}`);
  seen.add(testCase.id);
  const graph = normalizeGraph(testCase.graph);
  validateGraph(graph);
  if (Object.keys(graph).length > corpus.max_vertices) throw new Error(`${testCase.id}: exceeds max_vertices`);

  const pythonColoring = runPython(graph);
  const sourceColorable = pythonColoring !== null;
  const sourceWitnessValid = pythonColoring === null ? null : validColoring(graph, pythonColoring);
  if (sourceWitnessValid === false) throw new Error(`${testCase.id}: Python returned invalid coloring`);

  const metta = runMetta(graph);
  const mettaColorable = metta.rendered.length > 0;
  const firstMetta = mettaColorable ? parseColoring(metta.rendered[0], Object.keys(graph)) : null;
  const mettaWitnessValid = firstMetta === null ? null : validColoring(graph, firstMetta);
  if (mettaWitnessValid === false) throw new Error(`${testCase.id}: MeTTa returned invalid coloring: ${metta.rendered[0]}`);

  const agrees = sourceColorable === mettaColorable;
  if (!agrees) mismatchCount += 1;
  cases.push({
    id: testCase.id,
    vertex_count: Object.keys(graph).length,
    edge_count: undirectedEdges(graph, Object.keys(graph).sort()).length,
    graph_hash: sha256(JSON.stringify(graph)),
    source: {
      colorable: sourceColorable,
      witness_valid: sourceWitnessValid,
      witness: pythonColoring,
    },
    metta: {
      colorable: mettaColorable,
      witness_valid: mettaWitnessValid,
      result_count: metta.rendered.length,
      first_result: metta.rendered[0] ?? null,
      program_hash: sha256(metta.program),
    },
    agrees,
  });
}

const evidence = {
  witness: "WIT-DIFFERENTIAL",
  schema: "mettafy-differential-execution-v1",
  repository_sha: repoSha(),
  corpus: {
    path: "certification/differential-four-color-v1.json",
    sha256: sha256(corpusBytes),
    version: corpus.version,
    case_count: corpus.cases.length,
    max_vertices: corpus.max_vertices,
  },
  runtimes: {
    python: spawnSync(process.env.PYTHON || "python", ["--version"], { encoding: "utf8" }).stdout.trim(),
    mettascript_commit: METTASCRIPT_COMMIT,
  },
  claim: corpus.claim_boundary,
  non_claims: corpus.non_claims,
  threshold: { maximum_mismatches: 0 },
  mismatch_count: mismatchCount,
  cases,
  result: mismatchCount === 0 ? "pass" : "fail",
};

fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(outPath, `${JSON.stringify(evidence, null, 2)}\n`, "utf8");
if (mismatchCount !== 0) {
  console.error(`Differential witness failed: ${mismatchCount} mismatch(es). Evidence: ${outPath}`);
  process.exit(1);
}
console.log(`Differential witness passed: ${cases.length} cases, 0 mismatches.`);
