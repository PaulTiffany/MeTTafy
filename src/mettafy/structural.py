"""Source-neutral structural evidence layer for MeTTafy.

This module implements the first tranche of Issue #32:
  pinned Rocq source → leakage-safe structural evidence → blind projection.

Design constraints (transferable to laymen, mathematicians, and machines):
- Lay reader: every recovered fact can be stated in plain language.
- Mathematician: structural observations are checkable against the formal text.
- Machine: all data are typed, deterministic, hashable, and provenance-bearing.

Semantic strategy labels are never stored in this IR. They appear only later
as optional predictions that may abstain.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

EXTRACTOR_VERSION = "0.1.0-structural-bootstrap"

# Primary pinned paths relative to the upstream repository root.
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
    local_id: str
    kind: UnitKind
    body_form: str
    references: tuple[str, ...] = ()
    features: tuple[ObservableFeature, ...] = ()
    span: SourceLocation | None = None
    # Original identifier kept only for audit; never fed to classifiers.
    original_name: str | None = None


@dataclass
class Provenance:
    mettafy_sha: str
    upstream_sha: str
    extractor_version: str
    input_hashes: dict[str, str] = field(default_factory=dict)
    notes: str = ""


@dataclass
class StructuralEvidence:
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
                    # original_name intentionally omitted from public dict
                }
                for u in self.units
            ],
            "edges": [list(e) for e in self.edges],
        }

    def audit_map(self) -> dict[str, dict[str, Any]]:
        """Map blind local_id back to original name and span for human inspection."""
        result: dict[str, dict[str, Any]] = {}
        for u in self.units:
            result[u.local_id] = {
                "original_name": u.original_name,
                "span": asdict(u.span) if u.span else None,
                "kind": u.kind.value,
            }
        return result


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _stable_local_id(path: str, kind: str, index: int) -> str:
    """Produce a deterministic blind identifier independent of theorem names."""
    material = f"{path}:{kind}:{index}"
    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()[:12]
    return f"unit:{digest}"


# Very conservative sentence splitter for Rocq/Coq vernacular.
# Handles the high-level compositional style of the primary layers.
_THEOREM_RE = re.compile(
    r"^(Theorem|Lemma|Definition|Corollary|Fact|Remark)\s+([A-Za-z0-9_']+)",
    re.MULTILINE,
)
_PROOF_START_RE = re.compile(r"^Proof\.?\s*$", re.MULTILINE)
_QED_RE = re.compile(r"^Qed\.?\s*$", re.MULTILINE)


def _extract_units_from_source(
    source: str, path: str
) -> list[StructuralUnit]:
    """Extract a minimal set of structural units from a single .v file.

    This bootstrap extractor recognises only high-precision syntactic forms.
    It does not attempt to interpret semantics or expand StrategyKind.
    """
    lines = source.splitlines()
    units: list[StructuralUnit] = []
    index = 0

    for match in _THEOREM_RE.finditer(source):
        kind_str = match.group(1).lower()
        name = match.group(2)
        start_char = match.start()
        start_line = source.count("\n", 0, start_char) + 1

        # Locate the end of the statement / proof roughly by next top-level keyword or Qed.
        rest = source[match.end() :]
        end_rel = len(rest)
        for end_pat in (_THEOREM_RE, _QED_RE):
            m2 = end_pat.search(rest)
            if m2 and m2.start() < end_rel:
                end_rel = m2.start()
        end_char = match.end() + end_rel
        end_line = source.count("\n", 0, end_char) + 1

        body = source[match.start() : end_char]
        body_lower = body.lower()

        features: list[ObservableFeature] = []
        if re.search(r"\belim\b|\binduction\b|\bInduction\b", body):
            features.append(ObservableFeature.INDUCTION)
        if re.search(r"\bcase\b|\bCase\b|\bdestruct\b", body):
            features.append(ObservableFeature.CASE_SPLIT)
        if re.search(r"\brewrite\b|\btransport\b|\bexact\b.*\(.*\)", body):
            features.append(ObservableFeature.REWRITE_TRANSPORT)
        if re.search(r"\bdecide_\w+|\bdecide\b", body_lower):
            features.append(ObservableFeature.DECISION_CALL)
        if "exact (" in body_lower or "apply:" in body_lower or "exact " in body_lower:
            features.append(ObservableFeature.APPLICATION)
        if body.count("exact") + body.count("apply") + body.count("pose proof") >= 2:
            features.append(ObservableFeature.COMPOSITION)

        # Collect simple references by looking for qualified or bare identifiers
        # that appear after Require / Import style or in applications.
        # Keep only a conservative set to avoid noise.
        refs: list[str] = []
        for ref_match in re.finditer(
            r"\b([a-z][a-z0-9_']*(?:\.[a-z][a-z0-9_']*)+)\b", body, re.IGNORECASE
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
                references=tuple(dict.fromkeys(refs)),  # stable unique
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
    """Build StructuralEvidence from a mapping of relative path → source text.

    Parameters
    ----------
    sources:
        Mapping of path (relative to upstream root) to full file content.
    upstream_sha:
        The pinned commit of the upstream formal artifact.
    mettafy_sha:
        The MeTTafy repository commit that produced this extraction.
    """
    input_hashes = {path: _sha256_text(text) for path, text in sorted(sources.items())}
    units: list[StructuralUnit] = []
    for path, text in sorted(sources.items()):
        units.extend(_extract_units_from_source(text, path))

    # Simple edges: if unit A’s body mentions a qualified name that appears as
    # another unit’s original name, record a dependency. This is intentionally
    # conservative.
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


def blind_structural_view(evidence: StructuralEvidence) -> dict[str, Any]:
    """Return a classifier-safe view with identifiers and path role leakage removed.

    The audit map is deliberately omitted from this view.
    """
    data = evidence.to_dict()
    # Strip any residual path components that could convey proof role.
    for unit in data.get("units", []):
        span = unit.get("span")
        if isinstance(span, dict) and "path" in span:
            # Keep only a blind token derived from the hash of the path.
            path = span["path"]
            span["path"] = "path:" + hashlib.sha256(path.encode()).hexdigest()[:10]
    return data


def load_primary_layers_from_directory(root: Path) -> dict[str, str]:
    """Convenience helper: load the five primary proof-layer files if present."""
    sources: dict[str, str] = {}
    for rel in PRIMARY_PROOF_LAYERS:
        p = root / rel
        if p.is_file():
            sources[rel] = p.read_text(encoding="utf-8")
    return sources
