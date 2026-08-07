# Product engineering contract

MeTTafy is still a pre-alpha research project. That describes the maturity of its scientific claims and public API. It does **not** lower the engineering bar for artifacts we publish.

The product rule is simple:

> A green build must mean that the artifact a user receives is reproducible, attributable, installable, and usable at the boundary we claim to support.

This document defines engineering hardening. The stricter definition of **certified green**—including exact unit-test families, semantic benchmarks, thresholds, and certificate evidence—is maintained in [`production-certification.md`](production-certification.md) and [`certification/program-v1.json`](../certification/program-v1.json). CI success is evidence; it is not by itself a production certificate.

## Release gates

### Python product

Every change to `main` must keep the supported Python surface healthy across Python 3.11–3.14:

- source lint passes;
- static type checks pass;
- unit and deterministic-build tests pass;
- source and wheel distributions build successfully;
- package metadata validates strictly;
- the built wheel installs into an isolated environment;
- the installed `mettafy` CLI successfully analyzes the checked-in bootstrap fixture;
- the runtime dependency graph is audited for known vulnerabilities.

A source checkout that works while the built wheel fails is a product failure.

### Pages product

The teaching site is a product surface, not generated documentation that is assumed to work because HTML was emitted.

Before deployment, CI must:

1. check out MesTTo/MeTTaScript at the exact pinned source commit;
2. verify that commit before building;
3. use the upstream-pinned pnpm version and frozen lockfile;
4. build `@mettascript/grapher` successfully;
5. require the expected Grapher bundle and upstream license;
6. build the MeTTafy site twice and require byte-identical output;
7. record SHA-256 and byte size for the deployed upstream bundle and license;
8. serve the generated `_site` artifact locally;
9. open the real site in Chromium;
10. require every primary page and internal link to resolve;
11. fail on browser console, page, and request errors;
12. require both `<metta-grapher>` elements to upgrade and mount real SVG canvases;
13. call the mounted Grapher's supported `playTrace()` reduction API, require at least two states, call `traceForward()`, and verify that the trace index advances;
14. verify legacy public URLs continue to resolve.

A successful static build with a broken browser integration is a failed release.

## Supply-chain policy

- GitHub Actions are pinned to full commit SHAs.
- Third-party source integrations are pinned to exact commits.
- Upstream lockfiles are honored when building upstream projects.
- Required licenses and attribution travel with deployed third-party artifacts.
- The deployed artifact records cryptographic integrity metadata for shipped third-party bytes.
- Dependency updates remain reviewable through Dependabot rather than silently floating at build time.

Pinning is not proof of safety. It makes change explicit and reviewable.

## Authority boundary

Engineering verification and scientific verification are different gates.

A reproducible build does not prove MeTTafy's semantic interpretation is correct. A browser smoke test does not prove the Four Color Theorem. A learned strategy label does not establish theorem validity.

For formal exemplars:

> Prediction may guide search; verification governs acceptance.

The upstream formal checker remains the authority for theorem validity. MeTTafy's evidence, strategy labels, visualizations, and explanations remain separately challengeable interpretations.

## Failure behavior

Production behavior should fail visibly and locally:

- missing required vendor artifacts stop the build;
- wrong upstream commits stop the build;
- broken internal links stop deployment;
- failed browser requests stop deployment;
- an inert Grapher stops deployment;
- package installation or CLI failure stops the Python release gate;
- unsupported semantic structure should produce abstention or explicit uncertainty, not invented confidence.

Fallbacks are for resilience and accessibility, not for hiding failures in a claimed primary integration.

## Still to harden

The current gates are the beginning of the product bar, not a declaration that MeTTafy is finished. Follow-on hardening includes:

- repository branch protection with required checks;
- a first-class lock and hash policy for MeTTafy's own development/release dependencies;
- SBOM and release artifact attestations;
- automated accessibility auditing beyond the current keyboard/reduced-motion-friendly fallback;
- explicit performance budgets for the web surface and larger exemplars;
- release/versioning automation and rollback procedure;
- privacy-preserving operational diagnostics if client-side telemetry is ever introduced;
- sandbox and resource-limit policy before untrusted source execution becomes a supported product feature;
- evidence-backed structural extraction for Four Color, replacing held-out annotations as the primary machine-produced result.

The hardening principle is continuous: every new supported boundary must gain an executable gate before it becomes a product promise.
