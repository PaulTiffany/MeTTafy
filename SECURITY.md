# Security Policy

MeTTafy is pre-alpha research software. It should not yet be treated as a security boundary or trusted execution environment.

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
- whether untrusted source programs, generated MeTTa, subprocesses, filesystem access, network access, or third-party runtimes are involved;
- a proposed mitigation if known.

## Security boundaries

MeTTafy analyzes and may eventually execute or transform programs. Treat all submitted source code and generated artifacts as potentially untrusted. Future runtime integrations must document sandbox assumptions explicitly; semantic equivalence or successful verification does not imply safety.

Dependency and workflow changes should use pinned or reviewable versions where practical and preserve the principle of least privilege for automation tokens.
