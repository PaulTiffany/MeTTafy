import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { MeTTa } from "../_vendor/MeTTaScript/packages/hyperon/dist/index.js";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");
const outDir = path.join(root, "artifacts", "witnesses");
fs.mkdirSync(outDir, { recursive: true });

const targetPath = path.join(root, "exemplars", "four_color", "high_level_strategy.metta");
const surfacePath = path.join(root, "exemplars", "four_color", "proof_surface.metta");
const demoPath = path.join(root, "_site", "four-color-demo.metta");
const target = fs.readFileSync(targetPath, "utf8");
const surface = fs.readFileSync(surfacePath, "utf8");
const demo = fs.readFileSync(demoPath, "utf8");

const failures = [];
const parser = new MeTTa();
let parsed = [];
try {
  parsed = parser.parseAll(target);
} catch (error) {
  failures.push(`semantic target parse failed: ${String(error)}`);
}
if (parsed.length < 10) failures.push(`semantic target parsed only ${parsed.length} atoms`);

const surfaceParser = new MeTTa();
let parsedSurface = [];
try {
  parsedSurface = surfaceParser.parseAll(surface);
} catch (error) {
  failures.push(`proof surface parse failed: ${String(error)}`);
}
if (parsedSurface.length < 50) {
  failures.push(`proof surface parsed only ${parsedSurface.length} atoms`);
}

const runtime = new MeTTa();
let reduction = [];
try {
  runtime.run(demo);
  reduction = runtime.run("!(pipeline finite-map)");
} catch (error) {
  failures.push(`demo execution failed: ${String(error)}`);
}
const rendered = reduction.flat().map(String);
if (!rendered.some((value) => value.includes("compactness-extension"))) {
  failures.push(`expected compactness-extension in reduction result, got ${JSON.stringify(rendered)}`);
}

const evidence = {
  witness: "WIT-METTA-RUNTIME",
  audience: "MeTTa ecosystem integrator",
  claim: "The checked Four Color semantic artifact and frozen Track-B proof surface parse under the pinned MeTTaScript Hyperon runtime, and the executable teaching projection reduces.",
  non_claims: [
    "semantic annotations are correct",
    "the proof surface establishes theorem validity",
    "MeTTaScript is the only supported MeTTa runtime",
    "the teaching projection is the Four Color proof",
  ],
  runtime_source_commit: "abe13439196bccdb48b6636773a46ec9772a7aaf",
  parsed_atom_count: parsed.length,
  proof_surface_atom_count: parsedSurface.length,
  reduction_results: rendered,
  failures,
  result: failures.length === 0 ? "pass" : "fail",
};
fs.writeFileSync(
  path.join(outDir, "metta-runtime.json"),
  `${JSON.stringify(evidence, null, 2)}\n`,
  "utf8",
);
if (failures.length) {
  console.error(failures.join("; "));
  process.exit(1);
}
console.log(
  `MeTTa runtime witness passed: ${parsed.length} strategy atoms; ${parsedSurface.length} proof-surface atoms; reduction reached compactness-extension.`,
);
