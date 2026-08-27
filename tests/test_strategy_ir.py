from __future__ import annotations

import pytest

from mettafy.active_inference_boundary import InferenceEpisode, instantiate, void_count
from mettafy.color_construction import ConstructionState
from mettafy.strategy_ir import (
    Answer,
    Ask,
    CommitOrNot,
    RoleplayEpisode,
    See,
    StrategySignature,
    StrategySnapshot,
    amortize_first_move,
    begin_hypothetical,
    first_repeated_strategy,
    imagine_commit,
    quotient_strategy_trace,
)


def chain_state() -> ConstructionState:
    graph = {
        "a": ("b",),
        "b": ("a", "c"),
        "c": ("b", "d"),
        "d": ("c",),
    }
    return ConstructionState(graph, {"a": 0})


def test_levels_of_thinking_reduce_imagined_voids_without_advancing_reality() -> None:
    """INFERENCE: nested hypothetical commitments are not construction turns."""

    realized = chain_state()
    root = begin_hypothetical(realized)
    first = imagine_commit(root, "b", 1)
    second = imagine_commit(first.after, "c", 0)
    third = imagine_commit(second.after, "d", 1)

    assert root.realized_voids == 3
    assert first.after.realized_voids == 3
    assert second.after.realized_voids == 3
    assert third.after.realized_voids == 3

    assert root.imagined_voids == 3
    assert first.after.imagined_voids == 2
    assert second.after.imagined_voids == 1
    assert third.after.imagined_voids == 0

    assert void_count(realized) == 3
    assert dict(realized.coloring) == {"a": 0}
    assert first.after.depth == 1
    assert second.after.depth == 2
    assert third.after.depth == 3


def test_roleplay_is_sequential_observation_of_one_same_turn_root() -> None:
    """INFERENCE: SEE/ASK/ANSWER serializes thought, not construction history."""

    realized = chain_state()
    root = begin_hypothetical(realized)
    first = imagine_commit(root, "b", 1)
    second = imagine_commit(first.after, "c", 0)

    start_signature = StrategySignature(
        observables=(("focus", "b"),),
        available_probes=("follow-b",),
        options=("b=1",),
    )
    reply_signature = StrategySignature(
        observables=(("focus", "c"),),
        available_probes=("follow-c",),
        response_classes=("continues",),
        options=("c=0",),
    )
    start = StrategySnapshot(root, start_signature)
    reply = StrategySnapshot(first.after, reply_signature)
    deeper = StrategySnapshot(second.after, reply_signature)

    episode = RoleplayEpisode(
        realized=realized,
        events=(
            See(start),
            Ask(start, "follow-b"),
            Answer(reply, "follow-b", "continues"),
            CommitOrNot(deeper, "b", 1, "commit"),
        ),
    )

    assert episode.sequential_observations == 4
    assert episode.max_level_of_thinking == 2
    assert episode.construction_voids == 3
    assert void_count(realized) == 3


def test_strategy_trace_quotients_repeated_concrete_positions() -> None:
    """INFERENCE: repeated proof-relevant states close a loop instead of unrolling it."""

    realized = chain_state()
    root = begin_hypothetical(realized)
    first = imagine_commit(root, "b", 1)
    second = imagine_commit(first.after, "c", 0)

    class_a = StrategySignature(
        observables=(("shape", "vertical"),),
        available_probes=("cross",),
        response_classes=("left", "right"),
    )
    class_b = StrategySignature(
        observables=(("shape", "mirror"),),
        available_probes=("return",),
        response_classes=("same",),
    )
    snapshots = (
        StrategySnapshot(root, class_a),
        StrategySnapshot(first.after, class_b),
        StrategySnapshot(second.after, class_b),
        StrategySnapshot(first.after, class_a),
    )

    classes = quotient_strategy_trace(snapshots)
    assert tuple(item.signature for item in classes) == (class_a, class_b)
    assert classes[0].members == (0, 3)
    assert classes[1].members == (1, 2)
    assert first_repeated_strategy(snapshots) == (1, 2)


def test_only_first_imagined_move_may_cross_the_real_turn_boundary() -> None:
    """BRIDGE: deeper MTG-style thinking cannot skip construction turns."""

    realized = chain_state()
    root = begin_hypothetical(realized)
    first = imagine_commit(root, "b", 1)
    second = imagine_commit(first.after, "c", 0)

    episode = InferenceEpisode(realized=realized, focus="b")
    certificate = amortize_first_move(episode, first)
    after = instantiate(certificate)

    assert after.coloring["b"] == 1
    assert void_count(after) == void_count(realized) - 1
    assert dict(realized.coloring) == {"a": 0}

    with pytest.raises(ValueError, match="only the first imagined move"):
        amortize_first_move(InferenceEpisode(realized=realized, focus="c"), second)


def test_imagined_commit_cannot_rewrite_realized_colors() -> None:
    """NEGATIVE: imagination may extend a possible future, never edit the actual past."""

    realized = chain_state()
    root = begin_hypothetical(realized)

    with pytest.raises(ValueError, match="already committed"):
        imagine_commit(root, "a", 2)
