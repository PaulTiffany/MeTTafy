from __future__ import annotations

from mettafy.hyperon_witness import (
    LivenessDecision,
    StateLivenessProbe,
    assess_state_liveness,
    execution_links,
    trace_from_record,
)

SOURCE = """
(likes Sam pizza)
!(match &self (likes Sam $f) $f)
!(add-atom &self (likes Sam sushi))
!(match &self (likes Sam $f) $f)
!(remove-atom &self (likes Sam sushi))
!(match &self (likes Sam $f) $f)
""".strip()

PROBE = StateLivenessProbe(
    dependency_id="fixture:likes-sushi",
    baseline_query_index=0,
    perturbed_query_index=2,
    restored_query_index=4,
    mutation_step_index=2,
    restoration_step_index=4,
)


def _record() -> dict:
    return {
        "ok": True,
        "engine": "hyperon",
        "engine_version": "0.2.10",
        "results": [
            ["pizza"],
            [],
            ["pizza", "sushi"],
            [],
            ["pizza"],
        ],
        "atoms": [{"atom": "(likes Sam pizza)", "metatype": "ExpressionAtom"}],
        "steps": [
            {
                "form": "(likes Sam pizza)",
                "results": [],
                "added": ["(likes Sam pizza)"],
                "removed": [],
            },
            {"form": "(match ...)", "results": ["pizza"], "added": [], "removed": []},
            {
                "form": "(add-atom ...)",
                "results": [],
                "added": ["(likes Sam sushi)"],
                "removed": [],
            },
            {
                "form": "(match ...)",
                "results": ["pizza", "sushi"],
                "added": [],
                "removed": [],
            },
            {
                "form": "(remove-atom ...)",
                "results": [],
                "added": [],
                "removed": ["(likes Sam sushi)"],
            },
            {"form": "(match ...)", "results": ["pizza"], "added": [], "removed": []},
        ],
        "error": "",
    }


def test_execution_trace_adds_new_typed_runtime_relation_only_after_observation() -> None:
    trace = trace_from_record(SOURCE, _record())
    links = execution_links(trace)
    assert trace.ok is True
    assert [(edge.relation, edge.source_id, edge.target_id) for edge in links] == [
        ("executed_as", trace.artifact_id, trace.trace_id)
    ]


def test_liveness_requires_query_effect_and_restoration() -> None:
    trace = trace_from_record(SOURCE, _record())
    assessment = assess_state_liveness(trace, PROBE)
    assert assessment.decision is LivenessDecision.LIVE


def test_no_query_effect_is_not_called_dead_semantics() -> None:
    record = _record()
    record["results"][2] = ["pizza"]
    trace = trace_from_record(SOURCE, record)
    assessment = assess_state_liveness(trace, PROBE)
    assert assessment.decision is LivenessDecision.NOT_DEMONSTRATED


def test_failed_restoration_is_inconsistent_not_live() -> None:
    record = _record()
    record["results"][4] = ["sushi"]
    trace = trace_from_record(SOURCE, record)
    assessment = assess_state_liveness(trace, PROBE)
    assert assessment.decision is LivenessDecision.INCONSISTENT


def test_missing_state_delta_is_insufficient() -> None:
    record = _record()
    record["steps"][2]["added"] = []
    trace = trace_from_record(SOURCE, record)
    assessment = assess_state_liveness(trace, PROBE)
    assert assessment.decision is LivenessDecision.INSUFFICIENT


def test_unavailable_execution_never_gets_execution_link_or_liveness() -> None:
    record = _record()
    record["ok"] = False
    record["error"] = "ModuleNotFoundError: hyperon"
    trace = trace_from_record(SOURCE, record)
    assert execution_links(trace) == []
    assert assess_state_liveness(trace, PROBE).decision is LivenessDecision.UNAVAILABLE


def test_malformed_driver_record_fails_closed() -> None:
    trace = trace_from_record(SOURCE, {"ok": True})
    assert trace.ok is False
    assert trace.error.startswith("MalformedWitnessRecord:")
