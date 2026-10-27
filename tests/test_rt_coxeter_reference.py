#!/usr/bin/env python3
"""Bounded independent exact finite-field Coxeter and homology regression."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from experiments.rt_coxeter_audit_reference import (
    direction, quadratic, spread, geometric_face, edge_basis, face_boundary,
    edge_boundary, h1_dim, rank_mod, vec_add, execute, effect_swap_equal,
    run_reference,
)


class CoxeterRouteReferenceTests(unittest.TestCase):
    def test_s3_hexagon_is_cycle_and_one_face_kills_h1(self):
        case = run_reference()
        self.assertEqual((case["vertices"], case["edges"]), (6, 6))
        self.assertEqual(case["h1_no_hexagon"], 1)
        self.assertEqual(case["h1_with_hexagon"], 0)
        self.assertEqual(len(case["hexagon_boundary"]), 6)

    def test_square_braid_and_source_gate_f5(self):
        p = 5
        d3 = tuple(direction(i, p) for i in range(3))
        self.assertIsNotNone(geometric_face((0, 1, 2), d3, {1}, p))
        self.assertIsNone(geometric_face((0, 1, 2), d3, {0}, p))
        self.assertEqual(spread(d3[0], d3[1], p), 1)
        self.assertEqual(spread(d3[0], d3[0], p), 0)
        self.assertEqual(quadratic(d3[0], p), 1)
        d4 = tuple(direction(i, p) for i in range(4))
        self.assertIsNotNone(geometric_face((0, 1, 2, 3), d4, {1}, p,
                                            r=0, other=2))
        self.assertIsNone(geometric_face((0, 1, 2, 3), d4, {0}, p,
                                           r=0, other=2))
        with self.assertRaises(ValueError):
            geometric_face((0, 1, 2, 3), d4, {1}, p, r=0, other=1)
        null = (1, 0, 0, 0, 0, 0, 0, 0)
        self.assertIsNone(spread(null, d3[0], p))

    def test_formal_gate_does_not_imply_effect_equivalence(self):
        p = 5
        d = direction(0, p)
        zero = (0,) * 8
        assert spread(d, d, p) == 0
        translations = {
            0: lambda x: vec_add(x, d, p),
            1: lambda x: vec_add(x, d, p),
        }
        self.assertTrue(effect_swap_equal((0, 1), 0, zero, translations))
        stateful = {
            0: translations[0],
            1: lambda x: vec_add(x, tuple((1 + x[0]) * v % p for v in d), p),
        }
        self.assertFalse(effect_swap_equal((0, 1), 0, zero, stateful))
        self.assertNotEqual(execute((0, 1), zero, stateful),
                            execute((1, 0), zero, stateful))
        # Identical declared rays pass spread gate zero nevertheless.

    def test_common_reset_suffix_cannot_mask_unequal_prefix_effects(self):
        p = 5
        zero = (0,) * 8
        base = direction(0, p)
        ops = {
            0: lambda x: vec_add(x, base, p),
            1: lambda x: tuple((2 * v) % p for v in x),
            2: lambda x: zero,  # Non-injective: erases the difference.
        }
        # Final states match, but the adjacent operations fail exact equality.
        self.assertEqual(execute((0, 1, 2), zero, ops),
                         execute((1, 0, 2), zero, ops))
        self.assertFalse(effect_swap_equal((0, 1, 2), 0, zero, ops))
        self.assertTrue(effect_swap_equal((0, 1, 2), 1, zero, ops))

    def test_modular_rank_guards(self):
        self.assertEqual(rank_mod([[1, 2], [2, 4]], 5), 1)
        self.assertEqual(rank_mod([[0, 1], [1, 0]], 5), 2)
        self.assertEqual(rank_mod([[0, 0], [0, 0]], 5), 0)


if __name__ == "__main__":
    unittest.main()
