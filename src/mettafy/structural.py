"""Source-neutral structural evidence layer for MeTTafy.

Issue #32 tranche with type-level one-way membrane:

  raw StructuralEvidence (+ audit metadata)
      → blind_structural_view()
      → BlindStructuralEvidence   # literally cannot carry leakage fields
      → recognizer
      → Strategy / abstention
      → separately joined held-out evaluation

Semantic strategy labels are never stored in either IR.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

EXTRACTOR_VERSION = "0.1.1-structural-bootstrap"

PRIMARY_PROOF_LAYERS = (
    "theories/proof/fourcolor.v",
    "theories/proof/combinatorial4ct.v",
    "theories/proof/unavoidability.v",
    "theories/proof/reducibility.v",
    "theories/proof/discharge.v",
)


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
    """Raw unit — may hold audit-sensitive fields. Never pass to a recognizer."""

    local_id: str
    kind: UnitKind
    body_form: str
    references: tuple[str, ...] = ()
    features: tuple[ObservableFeature, ...] = ()
    span: SourceLocation | None = None
    original_name: str | None = None


@dataclass(frozen=True)
class BlindStructuralUnit:
    """Classifier-safe unit. Typed so leakage fields cannot be present."""

    local_id: str
    kind: UnitKind
    features: tuple[ObservableFeature, ...] = ()
    # Opaque tokens only — no recoverable path or identifier content.
    span_token: str = ""
    start_line: int = 0
    end_line: int = 0


@dataclass
class Provenance:
    mettafy_sha: str
    upstream_sha: str
    extractor_version: str
    input_hashes: dict[str, str] = field(default_factory=dict)
    notes: str = ""


@dataclass
class StructuralEvidence:
    """Raw evidence + audit side of the membrane."""

    provenance: Provenance
    units: list[StructuralUnit] = field(default_factory=list)
    edges: list[tuple[str, str]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "provenance": asdict(self.provenance),
            "units": [
                {
                    "local_id": u.local_id,
                    "kind": u.kind.value,
                    "body_form": u.body_form,
                    "references": list(u.references),
                    "features": [f.value for f in u.features],
                    "span": asdict(u.span) if u.span else None,
                }
                for u in self.units
            ],
            "edges": [list(e) for e in self.edges],
        }

    def audit_map(self) -> dict[str, dict[str, Any]]:
        result: dict[str, dict[str, Any]] = {}
        for u in self.units:
            result[u.local_id] = {
                "original_name": u.original_name,
                "span": asdict(u.span) if u.span else None,
                "kind": u.kind.value,
                "references": list(u.references),
            }
        return result


@dataclass(frozen=True)
class BlindStructuralEvidence:
    """One-way blind projection. Recognizers accept only this type."""

    provenance: Provenance
    units: tuple[BlindStructuralUnit, ...] = ()
    # Edges retain only blind local_ids.
    edges: tuple[tuple[str, str], ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "provenance": asdict(self.provenance),
            "units": [
                {
                    "local_id": u.local_id,
                    "kind": u.kind.value,
                    "features": [f.value for f in u.features],
                    "span_token": u.span_token,
                    "start_line": u.start_line,
                    "end_line": u.end_line,
                }
                for u in self.units
            ],
            "edges": [list(e) for e in self.edges],
        }


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _stable_local_id(path: str, kind: str, index: int) -> str:
    material = f"{path}:{kind}:{index}"
    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()[:12]
    return f"unit:{digest}"


def _strip_coq_comments(text: str) -> str:
    """Remove (* ... *) comments, including nested forms, before feature detection."""
    # Iterative non-greedy removal handles simple nesting adequately for bootstrap.
    prev = None
    while prev != text:
        prev = text
        text = re.sub(r"\(\*.*?\*\)", " ", text, flags=re.DOTALL)
    return text


_THEOREM_RE = re.compile(
    r"^(Theorem|Lemma|Definition|Corollary|Fact|Remark)\s+([A-Za-z0-9_']+)",
    re.MULTILINE,
)
_QED_RE = re.compile(r"^Qed\.?\s*$", re.MULTILINE)


def _extract_units_from_source(source: str, path: str) -> list[StructuralUnit]:
    units: list[StructuralUnit] = []
    index = 0

    for match in _THEOREM_RE.finditer(source):
        kind_str = match.group(1).lower()
        name = match.group(2)
        start_char = match.start()
        start_line = source.count("\n", 0, start_char) + 1

        rest = source[match.end() :]
        end_rel = len(rest)
        for end_pat in (_THEOREM_RE, _QED_RE):
            m2 = end_pat.search(rest)
            if m2 and m2.start() < end_rel:
                end_rel = m2.start()
        end_char = match.end() + end_rel
        end_line = source.count("\n", 0, end_char) + 1

        body = source[match.start() : end_char]
        # Feature detection must ignore comments.
        code_only = _strip_coq_comments(body)
        code_lower = code_only.lower()

        features: list[ObservableFeature] = []
        if re.search(r"\belim\b|\binduction\b", code_only):
            features.append(ObservableFeature.INDUCTION)
        if re.search(r"\bcase\b|\bdestruct\b", code_only):
            features.append(ObservableFeature.CASE_SPLIT)
        if re.search(r"\brewrite\b", code_only):
            features.append(ObservableFeature.REWRITE_TRANSPORT)
        if re.search(r"\bdecide_\w+|\bdecide_colorable\b", code_lower):
            features.append(ObservableFeature.DECISION_CALL)
        if re.search(r"\bexact\b|\bapply:?\b", code_lower):
            features.append(ObservableFeature.APPLICATION)
        app_count = len(re.findall(r"\bexact\b|\bapply:?\b|\bpose proof\b", code_lower))
        if app_count >= 2:
            features.append(ObservableFeature.COMPOSITION)

        refs: list[str] = []
        for ref_match in re.finditer(
            r"\b([a-z][a-z0-9_']*(?:\.[a-z][a-z0-9_']*)+)\b", code_only, re.IGNORECASE
        ):
            refs.append(ref_match.group(1))

        kind = {
            "theorem": UnitKind.THEOREM,
            "lemma": UnitKind.LEMMA,
            "definition": UnitKind.DEFINITION,
        }.get(kind_str, UnitKind.OTHER)

        local_id = _stable_local_id(path, kind.value, index)
        index += 1

        units.append(
            StructuralUnit(
                local_id=local_id,
                kind=kind,
                body_form=body.strip()[:400] + ("\u2026" if len(body.strip()) > 400 else ""),
                references=tuple(dict.fromkeys(refs)),
                features=tuple(features),
                span=SourceLocation(
                    path=path,
                    start_line=start_line,
                    end_line=end_line,
                    start_byte=start_char,
                    end_byte=end_char,
                ),
                original_name=name,
            )
        )

    return units


def extract_structural_evidence(
    sources: dict[str, str],
    *,
    upstream_sha: str,
    mettafy_sha: str = "unknown",
) -> StructuralEvidence:
    input_hashes = {path: _sha256_text(text) for path, text in sorted(sources.items())}
    units: list[StructuralUnit] = []
    for path, text in sorted(sources.items()):
        units.extend(_extract_units_from_source(text, path))

    name_to_id = {u.original_name: u.local_id for u in units if u.original_name}
    edges: list[tuple[str, str]] = []
    for u in units:
        for ref in u.references:
            short = ref.split(".")[-1]
            if short in name_to_id and name_to_id[short] != u.local_id:
                edges.append((u.local_id, name_to_id[short]))

    return StructuralEvidence(
        provenance=Provenance(
            mettafy_sha=mettafy_sha,
            upstream_sha=upstream_sha,
            extractor_version=EXTRACTOR_VERSION,
            input_hashes=input_hashes,
            notes=(
                "Bootstrap syntax-surface extractor. "
                "Does not claim completeness or semantic authority. "
                "Rocq remains the sole theorem-validity authority."
            ),
        ),
        units=units,
        edges=edges,
    )


def blind_structural_view(evidence: StructuralEvidence) -> BlindStructuralEvidence:
    """One-way projection. Result type cannot carry leakage fields."""
    blind_units: list[BlindStructuralUnit] = []
    for u in evidence.units:
        path = u.span.path if u.span else ""
        span_token = "span:" + hashlib.sha256(path.encode()).hexdigest()[:12]
        blind_units.append(
            BlindStructuralUnit(
                local_id=u.local_id,
                kind=u.kind,
                features=u.features,
                span_token=span_token,
                start_line=u.span.start_line if u.span else 0,
                end_line=u.span.end_line if u.span else 0,
            )
        )
    return BlindStructuralEvidence(
        provenance=evidence.provenance,
        units=tuple(blind_units),
        edges=tuple(evidence.edges),
    )


def load_primary_layers_from_directory(root: Path) -> dict[str, str]:
    sources: dict[str, str] = {}
    for rel in PRIMARY_PROOF_LAYERS:
        p = root / rel
        if p.is_file():
            sources[rel] = p.read_text(encoding="utf-8")
    return sources
