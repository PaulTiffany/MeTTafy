from __future__ import annotations

import ast
from dataclasses import dataclass

from .ir import Evidence, SourceSpan, Strategy, StrategyKind


@dataclass
class _FunctionFacts:
    name: str
    node: ast.FunctionDef | ast.AsyncFunctionDef
    recursive_calls: list[ast.Call]
    calls: list[ast.Call]
    assignments: list[ast.Assign | ast.AnnAssign | ast.AugAssign]
    restores: list[ast.Assign | ast.AnnAssign | ast.AugAssign]


def _span(filename: str, node: ast.AST) -> SourceSpan:
    return SourceSpan(
        filename=filename,
        start_line=getattr(node, "lineno", 1),
        end_line=getattr(node, "end_lineno", getattr(node, "lineno", 1)),
    )


def _call_name(call: ast.Call) -> str | None:
    func = call.func
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return None


def _target_key(node: ast.AST) -> str | None:
    try:
        return ast.unparse(node)
    except Exception:
        return None


def _collect_function_facts(fn: ast.FunctionDef | ast.AsyncFunctionDef) -> _FunctionFacts:
    calls = [node for node in ast.walk(fn) if isinstance(node, ast.Call)]
    recursive_calls = [call for call in calls if _call_name(call) == fn.name]
    assignments = [
        node
        for node in ast.walk(fn)
        if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign))
    ]

    # A conservative rollback signal: the same explicit target is assigned more than once.
    # It does not by itself establish backtracking; it is combined with recursion below.
    seen: dict[str, ast.AST] = {}
    restores: list[ast.Assign | ast.AnnAssign | ast.AugAssign] = []
    for assignment in assignments:
        targets: list[ast.AST] = []
        if isinstance(assignment, ast.Assign):
            targets = assignment.targets
        elif isinstance(assignment, ast.AnnAssign):
            targets = [assignment.target]
        elif isinstance(assignment, ast.AugAssign):
            targets = [assignment.target]
        for target in targets:
            key = _target_key(target)
            if key and key in seen:
                restores.append(assignment)
            elif key:
                seen[key] = assignment

    return _FunctionFacts(
        name=fn.name,
        node=fn,
        recursive_calls=recursive_calls,
        calls=calls,
        assignments=assignments,
        restores=restores,
    )


def analyze_source(source: str, filename: str = "<memory>") -> list[Strategy]:
    """Recover a small, evidence-backed strategy graph from Python source.

    v0.0.1 intentionally recognizes only high-precision bootstrap patterns.
    Unknown code is left unclassified rather than guessed.
    """

    tree = ast.parse(source, filename=filename)
    functions = [
        node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    facts = [_collect_function_facts(fn) for fn in functions]
    strategies: list[Strategy] = []

    # Recognize recursive search with state rollback/reassignment.
    for fact in facts:
        if fact.recursive_calls and fact.restores:
            evidence = [
                Evidence(
                    kind="recursive-call",
                    detail=f"{fact.name} calls itself",
                    span=_span(filename, fact.recursive_calls[0]),
                ),
                Evidence(
                    kind="state-reassignment",
                    detail="a state target is assigned more than once in the recursive function",
                    span=_span(filename, fact.restores[0]),
                ),
            ]
            strategies.append(
                Strategy(
                    id=f"strategy:{fact.name}:backtracking",
                    kind=StrategyKind.BACKTRACKING_SEARCH,
                    confidence=0.90,
                    evidence=evidence,
                )
            )

    # Recognize candidate-validation helpers called from a recursive search function.
    helper_names = {fact.name for fact in facts if not fact.recursive_calls}
    for fact in facts:
        if not fact.recursive_calls:
            continue
        for call in fact.calls:
            name = _call_name(call)
            if name in helper_names and name and any(
                token in name.lower() for token in ("valid", "safe", "allow", "constraint")
            ):
                strategies.append(
                    Strategy(
                        id=f"strategy:{fact.name}:constraint:{name}",
                        kind=StrategyKind.CONSTRAINT_PROPAGATION,
                        confidence=0.80,
                        evidence=[
                            Evidence(
                                kind="candidate-validation-call",
                                detail=f"recursive search calls validation helper {name}",
                                span=_span(filename, call),
                            )
                        ],
                    )
                )

    return strategies
