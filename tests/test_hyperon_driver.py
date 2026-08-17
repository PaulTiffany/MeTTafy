from __future__ import annotations

import sys
import types

import pytest

from mettafy.hyperon_driver import _extra, introspect


class _FakeAtom:
    def __init__(self, text: str) -> None:
        self._text = text

    def __str__(self) -> str:
        return self._text


class _FakeSpace:
    def __init__(self) -> None:
        self._atoms = [_FakeAtom("(seed)")]

    def add_atom(self, atom: _FakeAtom) -> None:
        self._atoms.append(atom)

    def remove_atom(self, text: str) -> None:
        self._atoms = [atom for atom in self._atoms if str(atom) != text]

    def get_atoms(self) -> list[_FakeAtom]:
        return list(self._atoms)


class _FakeMeTTa:
    def __init__(self) -> None:
        self._space = _FakeSpace()

    def space(self) -> _FakeSpace:
        return self._space

    def parse_all(self, source: str) -> list[_FakeAtom]:
        assert source == "fixture"
        return [
            _FakeAtom("(likes Sam pizza)"),
            _FakeAtom("(likes Sam sushi)"),
            _FakeAtom("!"),
            _FakeAtom("(match &self (likes Sam $f) $f)"),
            _FakeAtom("!"),
            _FakeAtom("(remove-atom &self (likes Sam sushi))"),
            _FakeAtom("(dessert)"),
        ]

    def evaluate_atom(self, atom: _FakeAtom) -> list[_FakeAtom]:
        if str(atom).startswith("(remove-atom"):
            self._space.remove_atom("(likes Sam sushi)")
            return []
        return [_FakeAtom("pizza"), _FakeAtom("sushi")]


def _inject(monkeypatch: pytest.MonkeyPatch) -> None:
    module = types.ModuleType("hyperon")
    module.MeTTa = _FakeMeTTa
    monkeypatch.setitem(sys.modules, "hyperon", module)


def test_introspect_three_channels_share_one_stateful_pass(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _inject(monkeypatch)
    record = introspect("fixture")

    assert record["ok"] is True
    assert record["results"] == [["pizza", "sushi"], []]
    assert [item["atom"] for item in record["atoms"]] == [
        "(seed)",
        "(likes Sam pizza)",
        "(dessert)",
    ]
    assert record["steps"][2]["results"] == ["pizza", "sushi"]
    assert record["steps"][3]["removed"] == ["(likes Sam sushi)"]
    assert record["steps"][4]["added"] == ["(dessert)"]


def test_introspect_import_failure_is_data(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setitem(sys.modules, "hyperon", None)
    record = introspect("fixture")
    assert record["ok"] is False
    assert record["results"] == []
    assert record["steps"] == []
    assert record["error"]


def test_extra_is_ordered_and_multiplicity_aware() -> None:
    assert _extra(["a", "b", "a"], ["a"]) == ["b", "a"]
