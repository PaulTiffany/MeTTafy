"""Source-neutral structural evidence for MeTTafy.

Issue #32 establishes a one-way membrane:

    raw StructuralEvidence + audit metadata
        -> blind_structural_view()
        -> BlindStructuralEvidence
        -> recognizer
        -> Strategy candidate / abstention
        -> separately joined held-out evaluation

The blind type cannot carry source text, source identifiers, source paths, or
per-file provenance. Semantic strategy labels are never stored in either IR.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

EXTRACTOR_VERSION = "0.2.0-structural-bootstrap"

PRIMARY_PROOF_LAYERS = (
    "theories/proof/fourcolor.v",
    "theories/proof/combinatorial4ct.v",
    "theories/proof/unavoidability.v",
    "theories/proof/reducibility.v",
    "theories/proof/discharge.v",
)

HIGH_LEVEL_PROOF_LAYERS = PRIMARY_PROOF_LAYERS[:2]


class UnitKind(str, Enum):
    THEOREM = "theorem"
    LEMMA = "lemma"
    DEFINITION = "definition"
    SECTION = "section"
    MODULE = "module"
    OTHER = "other"


class ObservableFeature(str, Enum):
    INDUCTION = "induction"
    CASE_SPLIT = "case_split"
    REWRITE_TRANSPORT = "rewrite_transport"
    RECURSION = "recursion"
    DECISION_CALL = "decision_call"
    EXTERNAL_BOUNDARY = "external_boundary"
    APPLICATION = "application"
    COMPOSITION = "composition"


@dataclass(frozen=True)
class SourceLocation:
    path: str
    start_line: int
    end_line: int
    start_byte: int = 0
    end_byte: int = 0


@dataclass(frozen=True)
class StructuralUnit:
    """Raw structural unit. It may contain audit-sensitive source material."""

    local_id: str
    kind: UnitKind
    body_form: str
    references: tuple[str, ...] = ()
    features: tuple[ObservableFeature, ...] = ()
    span: SourceLocation | None = None
    original_name: str | None = None


@dataclass(frozen=True)
class BlindStructuralUnit:
    """Classifier-safe unit with no source text, names, references, or paths."""

    local_id: str
    kind: UnitKind
    features: tuple[ObservableFeature, ...] = ()
    source_token: str = ""
    start_line: int = 0
    end_line: int = 0


@dataclass
class Provenance:
    """Full provenance retained on the audit side of the membrane."""

    mettafy_sha: str
    upstream_sha: str
    extractor_version: str
    input_hashes: dict[str, str] = field(default_factory=dict)
    notes: str = ""


@dataclass(frozen=True)
class BlindProvenance:
    """Classifier-safe provenance with source identity removed."""

    mettafy_sha: str
    extractor_version: str
    corpus_hash: str
    source_count: int


@dataclass
class StructuralEvidence:
    """Raw evidence plus source/audit metadata."""

    provenance: Provenance
    units: list[StructuralUnit] = field(default_factory=list)
    edges: list[tuple[str, str]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "provenance": asdict(self.provenance),
            "units": [
                {
                    "local_id": unit.local_id,
                    "kind": unit.kind.value,
                    "body_form": unit.body_form,
                    "references": list(unit.references),
                    "features": [feature.value for feature in unit.features],
                    "span": asdict(unit.span) if unit.span else None,
                }
                for unit in self.units
            ],
            "edges": [list(edge) for edge in self.edges],
        }

    def audit_map(self) -> dict[str, dict[str, Any]]:
        """Return raw-unit audit metadata. Never pass this mapping to recognizers."""
        result: dict[str, dict[str, Any]] = {}
        for unit in self.units:
            result[unit.local_id] = {
                "original_name": unit.original_name,
                "span": asdict(unit.span) if unit.span else None,
                "kind": unit.kind.value,
                "references": list(unit.references),
            }
        return result


@dataclass(frozen=True)
class BlindStructuralEvidence:
    """One-way projection accepted by semantic recognizers."""

    provenance: BlindProvenance
    units: tuple[BlindStructuralUnit, ...] = ()
    edges: tuple[tuple[str, str], ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "provenance": asdict(self.provenance),
            "units": [
                {
                    "local_id": unit.local_id,
                    "kind": unit.kind.value,
                    "features": [feature.value for feature in unit.features],
                    "source_token": unit.source_token,
                    "start_line": unit.start_line,
                    "end_line": unit.end_line,
                }
                for unit in self.units
            ],
            "edges": [list(edge) for edge in self.edges],
        }


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _corpus_hash(input_hashes: dict[str, str]) -> str:
    """Hash corpus content without embedding source paths in the material."""
    material = "\n".join(sorted(input_hashes.values()))
    return hashlib.sha256(material.encode("ascii")).hexdigest()


def _stable_raw_id(source_digest: str, kind: str, index: int) -> str:
    """Path-independent raw ID; blind projection replaces it with an ordinal ID."""
    material = f"{source_digest}:{kind}:{index}"
    digest = hashlib.sha256(material.encode("ascii")).hexdigest()[:16]
    return f"raw:{digest}"


def _strip_coq_comments(text: str) -> str:
    """Remove nested Rocq comments while preserving byte/line positions.

    Characters inside comments become spaces, except newlines which are retained.
    Unterminated comments fail closed rather than leaking documentary text into
    feature extraction.
    """
    output: list[str] = []
    depth = 0
    index = 0
    while index < len(text):
        if text.startswith("(*", index):
            depth += 1
            output.extend((" ", " "))
            index += 2
            continue
        if text.startswith("*)", index):
            if depth == 0:
                raise ValueError("unmatched Rocq comment terminator")
            depth -= 1
            output.extend((" ", " "))
            index += 2
            continue

        char = text[index]
        if depth:
            output.append("\n" if char == "\n" else " ")
        else:
            output.append(char)
        index += 1

    if depth:
        raise ValueError("unterminated Rocq comment")
    return "".join(output)


_THEOREM_RE = re.compile(
    r"^(Theorem|Lemma|Definition|Corollary|Fact|Remark)\s+([A-Za-z0-9_']+)",
    re.MULTILINE,
)
_QED_RE = re.compile(r"^Qed\.?\s*$", re.MULTILINE)
_APPLICATION_RE = re.compile(r"\b(?:exact|apply\s*:|apply|pose\s+proof)\b", re.IGNORECASE)
_DECISION_CALL_RE = re.compile(
    r"\b(?:have|pose\s+proof|exact|apply\s*:|apply)\b"
    r"[^.\n]*\bdecide_[A-Za-z0-9_']+\b\s+[@({A-Za-z0-9_]",
    re.IGNORECASE,
)
# Rocq identifiers may be qualified with dots, so a dot is not a safe command
# delimiter before the `as` binder. Keep the bootstrap pattern line-bounded.
_POSE_BINDING_RE = re.compile(
    r"\bpose\s+proof\b[^\n]*?\bas\s+"
    r"(?:\[([^\]]+)\]|([A-Za-z_][A-Za-z0-9_']*))",
    re.IGNORECASE,
)


def _has_dataflow_composition(code: str) -> bool:
    """Detect a bound result from one application consumed by a later one."""
    for match in _POSE_BINDING_RE.finditer(code):
        binding_text = match.group(1) or match.group(2) or ""
        names = re.findall(r"[A-Za-z_][A-Za-z0-9_']*", binding_text)
        tail = code[match.end() :]
        for name in names:
            if re.search(
                rf"\b(?:exact|apply\s*:|apply)\b[^.\n]*\b{re.escape(name)}\b",
                tail,
                re.IGNORECASE,
            ):
                return True
    return False


def _extract_units_from_source(
    source: str,
    path: str,
    source_digest: str,
) -> list[StructuralUnit]:
    """Extract bounded, mechanically observable structure from one Rocq file."""
    code_source = _strip_coq_comments(source)
    units: list[StructuralUnit] = []
    unit_index = 0

    for match in _THEOREM_RE.finditer(code_source):
        kind_text = match.group(1).lower()
        original_name = match.group(2)
        start_char = match.start()
        start_line = code_source.count("\n", 0, start_char) + 1

        rest = code_source[match.end() :]
        end_relative = len(rest)
        for pattern in (_THEOREM_RE, _QED_RE):
            candidate = pattern.search(rest)
            if candidate and candidate.start() < end_relative:
                end_relative = candidate.start()
        end_char = match.end() + end_relative
        end_line = code_source.count("\n", 0, end_char) + 1

        raw_body = source[match.start() : end_char]
        code_body = code_source[match.start() : end_char]

        features: list[ObservableFeature] = []
        if re.search(r"\belim\s*:|\binduction\b", code_body, re.IGNORECASE):
            features.append(ObservableFeature.INDUCTION)
        if re.search(r"\bcase(?:/[A-Za-z0-9_']+)?\b|\bdestruct\b", code_body, re.IGNORECASE):
            features.append(ObservableFeature.CASE_SPLIT)
        if re.search(r"\brewrite\b", code_body, re.IGNORECASE):
            features.append(ObservableFeature.REWRITE_TRANSPORT)
        if _DECISION_CALL_RE.search(code_body):
            features.append(ObservableFeature.DECISION_CALL)
        if _APPLICATION_RE.search(code_body):
            features.append(ObservableFeature.APPLICATION)
        if _has_dataflow_composition(code_body):
            features.append(ObservableFeature.COMPOSITION)

        references: list[str] = []
        for reference in re.finditer(
            r"\b([A-Za-z_][A-Za-z0-9_']*(?:\.[A-Za-z_][A-Za-z0-9_']*)+)\b",
            code_body,
        ):
            references.append(reference.group(1))

        kind = {
            "theorem": UnitKind.THEOREM,
            "lemma": UnitKind.LEMMA,
            "definition": UnitKind.DEFINITION,
        }.get(kind_text, UnitKind.OTHER)

        units.append(
            StructuralUnit(
                local_id=_stable_raw_id(source_digest, kind.value, unit_index),
                kind=kind,
                body_form=raw_body.strip()[:400]
                + ("…" if len(raw_body.strip()) > 400 else ""),
                references=tuple(dict.fromkeys(references)),
                features=tuple(features),
                span=SourceLocation(
                    path=path,
                    start_line=start_line,
                    end_line=end_line,
                    start_byte=start_char,
                    end_byte=end_char,
                ),
                original_name=original_name,
            )
        )
        unit_index += 1

    return units


def extract_structural_evidence(
    sources: dict[str, str],
    *,
    upstream_sha: str,
    mettafy_sha: str = "unknown",
) -> StructuralEvidence:
    """Extract raw evidence from path->source mappings with exact provenance."""
    if not sources:
        raise ValueError("at least one Rocq source is required")

    input_hashes = {
        path: _sha256_text(text) for path, text in sorted(sources.items())
    }
    units: list[StructuralUnit] = []
    for path, text in sorted(sources.items()):
        units.extend(_extract_units_from_source(text, path, input_hashes[path]))

    name_to_id = {unit.original_name: unit.local_id for unit in units if unit.original_name}
    edges: list[tuple[str, str]] = []
    for unit in units:
        for reference in unit.references:
            short_name = reference.split(".")[-1]
            target = name_to_id.get(short_name)
            if target and target != unit.local_id:
                edges.append((unit.local_id, target))

    return StructuralEvidence(
        provenance=Provenance(
            mettafy_sha=mettafy_sha,
            upstream_sha=upstream_sha,
            extractor_version=EXTRACTOR_VERSION,
            input_hashes=input_hashes,
            notes=(
                "Bootstrap syntax-surface extractor; incomplete by design. "
                "Rocq remains the sole theorem-validity authority."
            ),
        ),
        units=units,
        edges=edges,
    )


def _blind_maps(
    evidence: StructuralEvidence,
) -> tuple[dict[str, str], dict[str, str], list[StructuralUnit]]:
    """Create deterministic, source-name-independent tokens for blind projection."""
    paths = {
        unit.span.path
        for unit in evidence.units
        if unit.span is not None
    }
    ordered_paths = sorted(
        paths,
        key=lambda path: (evidence.provenance.input_hashes.get(path, ""), path),
    )
    source_tokens = {path: f"source:{index:03d}" for index, path in enumerate(ordered_paths)}

    ordered_units = sorted(
        evidence.units,
        key=lambda unit: (
            evidence.provenance.input_hashes.get(unit.span.path, "") if unit.span else "",
            unit.span.start_byte if unit.span else 0,
            unit.local_id,
        ),
    )
    id_map = {
        unit.local_id: f"unit:{index:05d}" for index, unit in enumerate(ordered_units)
    }
    return id_map, source_tokens, ordered_units


def blind_structural_view(evidence: StructuralEvidence) -> BlindStructuralEvidence:
    """Project raw evidence one-way into classifier-safe structural facts."""
    id_map, source_tokens, ordered_units = _blind_maps(evidence)
    blind_units = tuple(
        BlindStructuralUnit(
            local_id=id_map[unit.local_id],
            kind=unit.kind,
            features=unit.features,
            source_token=source_tokens.get(unit.span.path, "source:unknown")
            if unit.span
            else "source:unknown",
            start_line=unit.span.start_line if unit.span else 0,
            end_line=unit.span.end_line if unit.span else 0,
        )
        for unit in ordered_units
    )
    blind_edges = tuple(
        sorted(
            (id_map[source], id_map[target])
            for source, target in evidence.edges
            if source in id_map and target in id_map
        )
    )
    return BlindStructuralEvidence(
        provenance=BlindProvenance(
            mettafy_sha=evidence.provenance.mettafy_sha,
            extractor_version=evidence.provenance.extractor_version,
            corpus_hash=_corpus_hash(evidence.provenance.input_hashes),
            source_count=len(source_tokens),
        ),
        units=blind_units,
        edges=blind_edges,
    )


def blind_audit_map(evidence: StructuralEvidence) -> dict[str, dict[str, Any]]:
    """Join blind IDs back to raw metadata for evaluation/human audit only."""
    id_map, _, ordered_units = _blind_maps(evidence)
    result: dict[str, dict[str, Any]] = {}
    for unit in ordered_units:
        result[id_map[unit.local_id]] = {
            "raw_local_id": unit.local_id,
            "original_name": unit.original_name,
            "span": asdict(unit.span) if unit.span else None,
            "kind": unit.kind.value,
            "references": list(unit.references),
        }
    return result


def load_primary_layers_from_directory(
    root: Path,
    paths: tuple[str, ...] = PRIMARY_PROOF_LAYERS,
) -> dict[str, str]:
    """Load an explicit set of primary proof layers, failing closed if missing."""
    sources: dict[str, str] = {}
    missing: list[str] = []
    for relative_path in paths:
        path = root / relative_path
        if not path.is_file():
            missing.append(relative_path)
            continue
        sources[relative_path] = path.read_text(encoding="utf-8")
    if missing:
        raise FileNotFoundError(
            "missing pinned Rocq source layers: " + ", ".join(missing)
        )
    return sources
