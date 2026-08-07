# Security Policy

MeTTafy is a pre-alpha research project at the scientific and public-API layers. Published product surfaces are nevertheless expected to satisfy the engineering gates in `docs/product-hardening.md`.

Production engineering controls do **not** make MeTTafy a security boundary, sandbox, or trusted execution environment.

## Supported versions

Until the project reaches a tagged stable release, security fixes apply to the current `main` branch only.

## Reporting a vulnerability

Please do **not** publish exploit details, credentials, private data, or a working proof of concept in a public issue.

If GitHub private vulnerability reporting is enabled for this repository, use it. Otherwise, open a minimal public issue titled `Security contact requested` with no sensitive details so the maintainer can establish a private channel.

A useful report includes:

- affected commit or version;
- affected component;
- impact and realistic threat model;
- reproduction conditions;
- whether untrusted source programs, generated MeTTa, subprocesses, filesystem access, network access, browser execution, or third-party runtimes are involved;
- a proposed mitigation if known.

## Security boundaries

MeTTafy analyzes and may eventually execute or transform programs. Treat all submitted source code and generated artifacts as potentially untrusted.

Current browser assets are static and client-side, but a successful build or browser smoke test is not a sandbox guarantee. Future runtime integrations must document trust, isolation, resource, filesystem, and network assumptions explicitly before untrusted execution is advertised as supported.

Semantic equivalence, successful differential verification, a formal checker result, and operational safety are distinct claims. None should silently stand in for another.

## Supply chain

Product workflows should:

- use least-privilege automation permissions;
- pin GitHub Actions and source-built third-party integrations to exact commits;
- honor upstream lockfiles/toolchains;
- preserve third-party licenses and attribution;
- record integrity metadata for deployed third-party bytes;
- audit dependency graphs for known vulnerabilities;
- make dependency updates explicit and reviewable.

Pinning and hashing establish provenance and change control; they do not by themselves establish that code is safe.
