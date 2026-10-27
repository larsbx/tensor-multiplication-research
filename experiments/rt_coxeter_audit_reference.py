#!/usr/bin/env python3
"""Exact F_p Coxeter-route reference: boundary, H1, and effect-vs-gate.

This bounded model is deliberately separate from the canonical Mojo kernels.
A spread gate admits a *geometric* edge; it never establishes computational
equivalence without actual-prefix whole-state replay.
"""
from __future__ import annotations

from itertools import permutations
from typing import Callable

Vector = tuple[int, ...]
Ordering = tuple[int, ...]


def quadratic(x: Vector, p: int) -> int:
    if len(x) != 8 or p % 2 == 0:
        raise ValueError("expected eight coordinates and odd prime")
    return (2 * sum(x[i] * x[i + 4] for i in range(4))) % p


def pairing(x: Vector, y: Vector, p: int) -> int:
    return sum(x[i] * y[i + 4] + x[i + 4] * y[i] for i in range(4)) % p


def spread(x: Vector, y: Vector, p: int) -> int | None:
    a, b = quadratic(x, p), quadratic(y, p)
    den = a * b % p
    if not den:
        return None
    return ((den - pairing(x, y, p) ** 2) * pow(den, -1, p)) % p


def direction(i: int, p: int) -> Vector:
    if i not in range(4):
        raise ValueError("hyperbolic direction index")
    out = [0] * 8
    out[i] = 1
    out[i + 4] = pow(2, -1, p)
    assert quadratic(tuple(out), p) == 1
    return tuple(out)


def swapped(perm: Ordering, r: int) -> Ordering:
    if not (0 <= r < len(perm) - 1):
        raise ValueError("invalid adjacent-swap position")
    a = list(perm)
    a[r], a[r + 1] = a[r + 1], a[r]
    return tuple(a)


def gate_path(start: Ordering, steps: tuple[int, ...],
              directions: tuple[Vector, ...], accepted: set[int],
              p: int) -> list[Ordering] | None:
    if sorted(start) != list(range(len(directions))):
        return None
    path = [start]
    for r in steps:
        if not 0 <= r < len(start) - 1:
            return None
        a, b = start[r], start[r + 1]
        s = spread(directions[a], directions[b], p)
        if s is None or s not in accepted:
            return None
        start = swapped(start, r)
        path.append(start)
    return path


def face_paths(arity: int, r: int, other: int | None = None
               ) -> tuple[tuple[int, ...], tuple[int, ...]]:
    if other is None:
        if r < 0 or r + 2 >= arity:
            raise ValueError("invalid hexagon")
        return ((r, r + 1, r), (r + 1, r, r + 1))
    if not (0 <= r and r + 1 < other and other + 1 < arity):
        raise ValueError("invalid square")
    return ((r, other), (other, r))


def geometric_face(start: Ordering, directions: tuple[Vector, ...],
                   accepted: set[int], p: int,
                   r: int = 0, other: int | None = None
                   ) -> tuple[list[Ordering], list[Ordering]] | None:
    left_steps, right_steps = face_paths(len(start), r, other)
    a = gate_path(start, left_steps, directions, accepted, p)
    b = gate_path(start, right_steps, directions, accepted, p)
    if a is None or b is None or a[-1] != b[-1]:
        return None
    return a, b


def edge_basis(m: int) -> tuple[list[Ordering], list[tuple[Ordering, Ordering]]]:
    verts = list(permutations(range(m)))
    edges = sorted({tuple(sorted((v, swapped(v, r))))
                    for v in verts for r in range(m - 1)})
    return verts, edges


def face_boundary(a: list[Ordering], b: list[Ordering],
                  edges: list[tuple[Ordering, Ordering]]) -> list[int]:
    index = {e: i for i, e in enumerate(edges)}
    out = [0] * len(edges)
    for sign, path in ((1, a), (-1, b)):
        for u, v in zip(path, path[1:]):
            edge = tuple(sorted((u, v)))
            out[index[edge]] += sign * (1 if (u, v) == edge else -1)
    return out


def edge_boundary(verts: list[Ordering],
                  edges: list[tuple[Ordering, Ordering]]) -> list[list[int]]:
    vi = {v: i for i, v in enumerate(verts)}
    mat = [[0 for _ in edges] for _ in verts]
    for j, (u, v) in enumerate(edges):
        mat[vi[u]][j] = -1
        mat[vi[v]][j] = 1
    return mat


def rank_mod(matrix: list[list[int]], p: int) -> int:
    """Deterministic Gaussian elimination, no division by zero."""
    if not matrix:
        return 0
    a = [[x % p for x in row] for row in matrix]
    cols = len(a[0])
    if any(len(row) != cols for row in a):
        raise ValueError("jagged matrix")
    pivot_row = 0
    for col in range(cols):
        idx = next((i for i in range(pivot_row, len(a)) if a[i][col]), None)
        if idx is None:
            continue
        a[pivot_row], a[idx] = a[idx], a[pivot_row]
        pivot_inv = pow(a[pivot_row][col], -1, p)
        a[pivot_row] = [(x * pivot_inv) % p for x in a[pivot_row]]
        for i in range(len(a)):
            if i != pivot_row and a[i][col]:
                fac = a[i][col]
                a[i] = [(x - fac * y) % p for x, y in zip(a[i], a[pivot_row])]
        pivot_row += 1
        if pivot_row == len(a):
            break
    return pivot_row


def h1_dim(vertices: list[Ordering], edges: list[tuple[Ordering, Ordering]],
           face_columns: list[list[int]], p: int) -> int:
    b1 = edge_boundary(vertices, edges)
    b2 = [[column[i] for column in face_columns] for i in range(len(edges))]
    for col in face_columns:
        assert all(sum(row[j] * col[j] for j in range(len(edges))) % p == 0
                   for row in b1)
    return len(edges) - rank_mod(b1, p) - rank_mod(b2, p)


def vec_add(x: Vector, y: Vector, p: int) -> Vector:
    return tuple((a + b) % p for a, b in zip(x, y))


def execute(ordering: Ordering, initial: Vector,
            operations: dict[int, Callable[[Vector], Vector]]) -> Vector:
    state = initial
    for label in ordering:
        state = operations[label](state)
    return state


def effect_swap_equal(start: Ordering, r: int, initial: Vector,
                      operations: dict[int, Callable[[Vector], Vector]]) -> bool:
    # Only certify the two swapped operations AT THEIR ACTUAL PREFIX.
    # A common non-injective suffix can erase a genuine local discrepancy.
    if not 0 <= r < len(start) - 1:
        return False
    prefix_state = execute(start[:r], initial, operations)
    a, b = start[r], start[r + 1]
    ab = operations[b](operations[a](prefix_state))
    ba = operations[a](operations[b](prefix_state))
    return ab == ba


def run_reference() -> dict[str, object]:
    p = 5
    directions = tuple(direction(i, p) for i in range(3))
    verts, edges = edge_basis(3)
    face = geometric_face((0, 1, 2), directions, {1}, p)
    assert face is not None
    column = face_boundary(*face, edges)
    assert h1_dim(verts, edges, [], p) == 1
    assert h1_dim(verts, edges, [column], p) == 0
    assert geometric_face((0, 1, 2), directions, {0}, p) is None
    return {"field": "F5", "vertices": len(verts), "edges": len(edges),
            "hexagon_boundary": column, "h1_no_hexagon": 1,
            "h1_with_hexagon": 0}


if __name__ == "__main__":
    import json
    print(json.dumps(run_reference(), sort_keys=True, indent=2))
