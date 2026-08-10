from __future__ import annotations

from mettafy.reducibility_gate import (
    TraversalCertificate,
    assess_admissible_traversal,
    extract_blind_discharge_evidence,
)

PINNED_HIGH_LEVEL = r'''
Theorem four_color_hypermap G : planar_bridgeless G -> four_colorable G.
Proof.
move=> geoG; apply: cube_colorable.
have{geoG} geoGQ: planar_bridgeless_plain_precubic (cube G).
  split; last exact/cubic_precubic/cubic_cube.
  split; last exact: plain_cube.
  by split; [rewrite planar_cube | rewrite bridgeless_cube]; apply: geoG.
pose n := #|cube G|.+1; move: geoGQ (leqnn n); rewrite {1}/n.
elim: {G}n (cube G) => // n IHn G geoG; rewrite ltnS leq_eqVlt.
case/predU1P=> [Dn | /IHn]; [rewrite -{n}Dn in IHn | exact].
have [// | noncolG] := decide_colorable G.
by have [] := @unavoidability the_reducibility G.
Qed.
'''


def test_pinned_high_level_fixture_has_complete_discharge_surface() -> None:
    evidence = extract_blind_discharge_evidence(PINNED_HIGH_LEVEL)
    assert evidence.induction_descent is True
    assert evidence.decision_branch is True
    assert evidence.contradiction_elimination is True
    assert evidence.proof_application is True
    assert evidence.complete is True


def test_candidate_without_certificate_fails_closed() -> None:
    trace = assess_admissible_traversal(
        reduction_predicted=True,
        discharge_evidence=extract_blind_discharge_evidence(PINNED_HIGH_LEVEL),
    )
    assert trace.decision == "certificate_required"
    assert trace.certificate_present is False
    assert trace.certificate_valid is None


def test_boundary_change_rejects_certificate() -> None:
    certificate = TraversalCertificate.from_boundaries(
        boundary_before="outside:A-B-C",
        boundary_after="outside:A-C-B",
        measure_before=7,
        measure_after=6,
    )
    assert certificate.boundary_preserved is False
    assert certificate.strictly_decreases is True
    trace = assess_admissible_traversal(
        reduction_predicted=True,
        discharge_evidence=extract_blind_discharge_evidence(PINNED_HIGH_LEVEL),
        certificate=certificate,
    )
    assert trace.decision == "certificate_rejected"


def test_non_decreasing_measure_rejects_certificate() -> None:
    certificate = TraversalCertificate.from_boundaries(
        boundary_before="outside:A-B-C",
        boundary_after="outside:A-B-C",
        measure_before=7,
        measure_after=7,
    )
    assert certificate.boundary_preserved is True
    assert certificate.strictly_decreases is False
    trace = assess_admissible_traversal(
        reduction_predicted=True,
        discharge_evidence=extract_blind_discharge_evidence(PINNED_HIGH_LEVEL),
        certificate=certificate,
    )
    assert trace.decision == "certificate_rejected"


def test_negative_measure_fails_well_foundedness_guard() -> None:
    certificate = TraversalCertificate.from_boundaries(
        boundary_before="outside:A-B-C",
        boundary_after="outside:A-B-C",
        measure_before=0,
        measure_after=-1,
    )
    assert certificate.strictly_decreases is False
    assert certificate.valid is False


def test_valid_independent_certificate_promotes_admissible_traversal() -> None:
    certificate = TraversalCertificate.from_boundaries(
        boundary_before="outside:A-B-C",
        boundary_after="outside:A-B-C",
        measure_before=7,
        measure_after=6,
    )
    trace = assess_admissible_traversal(
        reduction_predicted=True,
        discharge_evidence=extract_blind_discharge_evidence(PINNED_HIGH_LEVEL),
        certificate=certificate,
    )
    assert certificate.valid is True
    assert trace.decision == "admissible_traversal"
    assert trace.certificate_valid is True


def test_incomplete_skeleton_rejects_even_valid_certificate() -> None:
    evidence = extract_blind_discharge_evidence(
        "Theorem x : P. Proof. have H := decide_colorable x. exact H. Qed."
    )
    certificate = TraversalCertificate.from_boundaries(
        boundary_before="same",
        boundary_after="same",
        measure_before=2,
        measure_after=1,
    )
    trace = assess_admissible_traversal(
        reduction_predicted=True,
        discharge_evidence=evidence,
        certificate=certificate,
    )
    assert trace.decision == "skeleton_incomplete"


def test_non_candidate_cannot_be_upgraded_by_certificate() -> None:
    certificate = TraversalCertificate.from_boundaries(
        boundary_before="same",
        boundary_after="same",
        measure_before=2,
        measure_after=1,
    )
    trace = assess_admissible_traversal(
        reduction_predicted=False,
        discharge_evidence=extract_blind_discharge_evidence(PINNED_HIGH_LEVEL),
        certificate=certificate,
    )
    assert trace.decision == "not_candidate"
