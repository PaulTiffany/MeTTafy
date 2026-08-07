# Acknowledgments

MeTTafy is intentionally built as a participant in the existing MeTTa, Hyperon, OpenCog, and program-analysis communities.

## OpenCog Hyperon / MeTTa

MeTTafy targets MeTTa and is conceptually downstream of the work of the OpenCog Hyperon community and the SingularityNET Foundation.

Upstream: https://github.com/trueagi-io/hyperon-experimental

The Hyperon reference implementation is distributed under the MIT License. Its source code is not copied into MeTTafy by default. If Hyperon is later included as a dependency or submodule, its copyright and license notices will be preserved in accordance with its license.

## MesTTo / MeTTaScript

MesTTo's MeTTaScript project is an important adjacent implementation and tooling ecosystem, including a TypeScript MeTTa runtime, eDSL, debugging, visualization, and Python/Prolog interoperability.

Upstream: https://github.com/MesTTo/MeTTaScript

MeTTaScript is distributed under the MIT License, copyright MesTTo. MeTTafy does not claim this work as its own. Future integration should prefer depending on or submoduling canonical upstream components rather than copying them.

## LogicMOO / metta-src-conversions

LogicMOO's `metta-src-conversions` repository is directly relevant prior art: it contains conventional symbolic/AI source programs alongside MeTTa conversions.

Upstream: https://github.com/logicmoo/metta-src-conversions

At repository bootstrap time, MeTTafy did not identify a clear repository-wide root license for this project. Accordingly, it is treated here as credited prior art only. No code from it should be copied, vendored, derived, or submoduled into MeTTafy until the applicable licensing terms are established for the material in question.

## Joern / Code Property Graph

Joern is a mature open-source platform for representing source code through Code Property Graphs and may provide an optional future multi-language structural front end.

Upstream: https://github.com/joernio/joern

If integrated, MeTTafy should use Joern through a clean adapter boundary and preserve all applicable upstream licensing and notices.

## Attribution policy

MeTTafy follows a simple rule:

> Credit ideas generously; copy code only with explicit permission from its license; prefer interoperating with canonical upstream implementations.

For any third-party component added to this repository, contributors should record:

- upstream project and canonical URL;
- exact version, tag, or commit when pinned;
- applicable license;
- whether it is a dependency, adapter target, git submodule, vendored code, or derived material;
- any required copyright or NOTICE text.

Corrections and additions to this file are welcome.
