#!/usr/bin/env python3
"""Exact, small-scale training-route audit with parameterizable tensor directions.

Research prototype, not an LLM equivalence oracle. Computation is over Q using
Fraction. A passing approximate diamond is NOT a topological 2-cell or proof
of endpoint equality. Exact diamonds alone generate path equivalences.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
from itertools import permutations
from json import dumps
from typing import Callable, Protocol

Scalar = Fraction
Vector = tuple[Scalar, ...]
Components = tuple[Vector, ...]


def vec(*xs: int | Fraction) -> Vector:
    return tuple(Fraction(x) for x in xs)


def plus(x: Vector, y: Vector) -> Vector:
    if len(x) != len(y):
        raise ValueError("dimension mismatch")
    return tuple(a + b for a, b in zip(x, y))


def minus(x: Vector, y: Vector) -> Vector:
    return plus(x, tuple(-v for v in y))


def dot(x: Vector, y: Vector) -> Scalar:
    if len(x) != len(y):
        raise ValueError("dimension mismatch")
    return sum((a * b for a, b in zip(x, y)), Fraction(0))


def sum_vectors(xs: Components, dimension: int) -> Vector:
    acc = (Fraction(0),) * dimension
    for x in xs:
        acc = plus(acc, x)
    return acc


def determinant(matrix: tuple[tuple[Scalar, ...], ...]) -> Scalar:
    """Division-free Leibniz expansion; sufficient for small research ranks."""
    n = len(matrix)
    if any(len(row) != n for row in matrix):
        raise ValueError("not square")
    total = Fraction(0)
    for p in permutations(range(n)):
        inversions = sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n))
        term = Fraction(-1 if inversions % 2 else 1)
        for i, j in enumerate(p):
            term *= matrix[i][j]
        total += term
    return total


def gram(xs: Components, ys: Components) -> Scalar:
    if len(xs) != len(ys) or not xs:
        raise ValueError("rank mismatch")
    return determinant(tuple(tuple(dot(x, y) for y in ys) for x in xs))


def spread(xs: Components, ys: Components) -> Scalar | None:
    """Exterior-power spread; rank 1 coincides with usual vector spread.

    Guard both Gram determinants. All inversions occur AFTER a nonzero check.
    """
    nx, ny = gram(xs, xs), gram(ys, ys)
    den = nx * ny
    if den == 0:
        return None
    mixed = gram(xs, ys)
    return Fraction(1) - mixed * mixed / den


@dataclass(frozen=True)
class Step:
    label: str
    source: Vector
    target: Vector
    factors: Components

    def displacement(self) -> Vector:
        return minus(self.target, self.source)


class DirectionModel(Protocol):
    name: str

    def extract(self, step: Step) -> Components: ...


@dataclass(frozen=True)
class VectorDirection:
    name: str = "vector"

    def extract(self, step: Step) -> Components:
        return (step.displacement(),)


@dataclass(frozen=True)
class FactorPlaneDirection:
    rank: int = 2
    name: str = "factor-plane"

    def extract(self, step: Step) -> Components:
        if len(step.factors) != self.rank:
            raise ValueError("wrong factor rank")
        if sum_vectors(step.factors, len(step.source)) != step.displacement():
            raise ValueError("factors fail to reconstruct displacement")
        return step.factors


@dataclass(frozen=True)
class Update:
    name: str
    components_at: Callable[[Vector], Components]

    def apply(self, state: Vector) -> Step:
        factors = self.components_at(state)
        if not factors or any(len(part) != len(state) for part in factors):
            raise ValueError("invalid component shape")
        return Step(self.name, state, plus(state, sum_vectors(factors, len(state))), factors)


@dataclass(frozen=True)
class Policy:
    max_edge_quadrance: Scalar
    max_endpoint_quadrance: Scalar
    max_spread: Scalar

    def __post_init__(self) -> None:
        if min(self.max_edge_quadrance, self.max_endpoint_quadrance, self.max_spread) < 0:
            raise ValueError("ordered Q policy needs nonnegative thresholds")


def scalar_text(x: Scalar | None) -> str | None:
    return None if x is None else str(x)


def vector_text(x: Vector) -> list[str]:
    return [str(a) for a in x]


def audit_diamond(anchor: Vector, i: Update, j: Update,
                  direction: DirectionModel, policy: Policy) -> dict:
    """Evaluate both actual orders, never manufacturing a common endpoint."""
    i_a, j_a = i.apply(anchor), j.apply(anchor)
    j_after_i = j.apply(i_a.target)
    i_after_j = i.apply(j_a.target)
    d_ij, d_ji = j_after_i.target, i_after_j.target
    edge_q = tuple(dot(s.displacement(), s.displacement())
                   for s in (i_a, j_a, j_after_i, i_after_j))
    endpoint_q = dot(minus(d_ij, d_ji), minus(d_ij, d_ji))
    si = spread(direction.extract(i_a), direction.extract(i_after_j))
    sj = spread(direction.extract(j_a), direction.extract(j_after_i))

    failures = []
    if any(q > policy.max_edge_quadrance for q in edge_q):
        failures.append("edge_energy")
    if si is None or sj is None:
        failures.append("null_direction")
    else:
        if si > policy.max_spread:
            failures.append("spread_i")
        if sj > policy.max_spread:
            failures.append("spread_j")
    if endpoint_q > policy.max_endpoint_quadrance:
        failures.append("endpoint")

    exact = d_ij == d_ji
    if failures:
        status = "rejected"
    elif exact:
        status = "certified_exact"
    else:
        status = "bounded_local_only"

    payload = {
        "schema": "training-route-diamond/v0",
        "model": direction.name,
        "updates": [i.name, j.name],
        "anchor": vector_text(anchor),
        "end_ij": vector_text(d_ij),
        "end_ji": vector_text(d_ji),
        "edge_quadrances": [str(q) for q in edge_q],
        "endpoint_quadrance": str(endpoint_q),
        "spread_i": scalar_text(si),
        "spread_j": scalar_text(sj),
        "policy": {
            "max_edge_quadrance": str(policy.max_edge_quadrance),
            "max_endpoint_quadrance": str(policy.max_endpoint_quadrance),
            "max_spread": str(policy.max_spread),
        },
        "status": status,
        "failures": failures,
    }
    # Hash is a reproducible transcript ID, NOT a cryptographic proof that the
    # update functions are faithful. Reexecution under pinned code is required.
    payload["transcript_sha256"] = sha256(
        dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return payload


def schedule_class_mass(audit: dict, p_ij: Scalar) -> dict[str, str]:
    """Probability masses only quotient when the local diamond is EXACT."""
    if not 0 <= p_ij <= 1:
        raise ValueError("probability outside [0,1]")
    if audit["status"] == "certified_exact":
        return {"ij~ji": "1"}
    return {"ij": str(p_ij), "ji": str(1 - p_ij)}


E0, E1, E2, E3 = (vec(*(int(i == j) for i in range(4))) for j in range(4))


def scaled(a: Scalar, x: Vector) -> Vector:
    return tuple(a * t for t in x)


def toy_updates(kind: str) -> tuple[Update, Update]:
    """Small structured 'tensor' updates (two exact additive components)."""
    i = Update("i", lambda state: (E0, E2))
    if kind == "commuting":
        j = Update("j", lambda state: (E1, E3))
    elif kind == "rescale":
        # Parallel transport of factor-plane, yet noncommuting endpoints.
        j = Update("j", lambda state: (scaled(1 + state[0] / 2, E1), E3))
    elif kind == "tilt":
        j = Update("j", lambda state: (plus(E1, scaled(state[0] / 2, E0)), E3))
    elif kind == "degenerate":
        j = Update("j", lambda state: (E1, E1))
    else:
        raise ValueError("unknown toy scenario")
    return i, j


def experiment() -> dict:
    policy = Policy(Fraction(5), Fraction(1, 4), Fraction(1, 10))
    records = []
    for case in ("commuting", "rescale", "tilt", "degenerate"):
        i, j = toy_updates(case)
        for model in (VectorDirection(), FactorPlaneDirection()):
            result = audit_diamond(vec(0, 0, 0, 0), i, j, model, policy)
            result["case"] = case
            result["schedule_mass"] = schedule_class_mass(result, Fraction(2, 3))
            records.append(result)
    return {"experiment": "exact-rational-parameterized-directions/v0",
            "records": records}


if __name__ == "__main__":
    print(dumps(experiment(), sort_keys=True, indent=2))
