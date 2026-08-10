from __future__ import annotations

from dataclasses import dataclass
import hashlib
from typing import Iterable

from .ir import ProvenanceEdge


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class RuntimeTrace:
    """Deterministic trace for an executable artifact-production boundary."""

    trace_id: str
    runtime_kind: str
    command: tuple[str, ...]
    exit_code: int
    stdout_sha256: str
    artifact_sha256: str

    @property
    def succeeded(self) -> bool:
        return self.exit_code == 0

    def to_dict(self) -> dict[str, object]:
        return {
            "trace_id": self.trace_id,
            "runtime_kind": self.runtime_kind,
            "command": list(self.command),
            "exit_code": self.exit_code,
            "stdout_sha256": self.stdout_sha256,
            "artifact_sha256": self.artifact_sha256,
            "succeeded": self.succeeded,
        }


@dataclass(frozen=True)
class RuntimeCertification:
    """Sibling provenance graph linking artifact, runtime trace, and witness."""

    runtime_trace: RuntimeTrace
    provenance: tuple[ProvenanceEdge, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "runtime_trace": self.runtime_trace.to_dict(),
            "provenance": [
                {
                    "relation": edge.relation,
                    "source_id": edge.source_id,
                    "target_id": edge.target_id,
                }
                for edge in self.provenance
            ],
        }


def certify_emission_runtime(
    *,
    artifact_id: str,
    artifact_text: str,
    command: Iterable[str],
    exit_code: int,
    stdout_text: str,
    witness_id: str,
) -> RuntimeCertification:
    """Create a typed provenance chain for the actual CLI emission boundary.

    This function does not claim that emitted MeTTa has been semantically executed.
    It certifies that a concrete command produced bytes matching the declared
    semantic artifact, and links that runtime event to a mechanical witness.
    """

    command_tuple = tuple(command)
    artifact_hash = sha256_text(artifact_text)
    stdout_hash = sha256_text(stdout_text)
    runtime_id = f"runtime:{artifact_hash[:16]}:{stdout_hash[:16]}"
    trace = RuntimeTrace(
        trace_id=runtime_id,
        runtime_kind="mettafy-cli-emission",
        command=command_tuple,
        exit_code=exit_code,
        stdout_sha256=stdout_hash,
        artifact_sha256=artifact_hash,
    )
    return RuntimeCertification(
        runtime_trace=trace,
        provenance=(
            ProvenanceEdge(
                relation="executed_as",
                source_id=artifact_id,
                target_id=runtime_id,
            ),
            ProvenanceEdge(
                relation="certified_by",
                source_id=runtime_id,
                target_id=witness_id,
            ),
        ),
    )
