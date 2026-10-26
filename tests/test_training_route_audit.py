#!/usr/bin/env python3
"""Regression checks for a toy exact-rational training route audit."""
import sys
import unittest
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from experiments.training_route_audit import (
    E0, E1, E2, E3, FactorPlaneDirection, Policy, VectorDirection,
    audit_diamond, gram, plus, schedule_class_mass, scaled, spread,
    toy_updates, vec,
)

POLICY = Policy(Fraction(5), Fraction(1, 4), Fraction(1, 10))
ZERO = vec(0, 0, 0, 0)


def run(case, direction):
    i, j = toy_updates(case)
    return audit_diamond(ZERO, i, j, direction, POLICY)


class TrainingRouteAuditTest(unittest.TestCase):
    def test_exact_commutations_are_valid_for_both_direction_models(self):
        for d in (VectorDirection(), FactorPlaneDirection()):
            with self.subTest(model=d.name):
                result = run("commuting", d)
                self.assertEqual(result["status"], "certified_exact")
                self.assertEqual(result["endpoint_quadrance"], "0")
                self.assertEqual(result["spread_i"], "0")
                self.assertEqual(result["spread_j"], "0")
                self.assertEqual(schedule_class_mass(result, Fraction(2, 3)), {"ij~ji": "1"})

    def test_parallel_directions_cannot_prove_endpoint_equivalence(self):
        for d in (VectorDirection(), FactorPlaneDirection()):
            with self.subTest(model=d.name):
                result = run("rescale", d)
                self.assertEqual(result["status"], "bounded_local_only")
                self.assertEqual(result["endpoint_quadrance"], "1/4")
                self.assertEqual(result["spread_i"], "0")
                self.assertEqual(result["failures"], [])
                self.assertEqual(
                    schedule_class_mass(result, Fraction(2, 3)),
                    {"ij": "2/3", "ji": "1/3"},
                )
        self.assertEqual(run("rescale", VectorDirection())["spread_j"], "1/26")
        self.assertEqual(run("rescale", FactorPlaneDirection())["spread_j"], "0")

    def test_tilt_fails_spread_even_at_accepted_endpoint_bound(self):
        for d, value in ((VectorDirection(), "1/9"),
                         (FactorPlaneDirection(), "1/5")):
            with self.subTest(model=d.name):
                result = run("tilt", d)
                self.assertEqual(result["status"], "rejected")
                self.assertEqual(result["endpoint_quadrance"], "1/4")
                self.assertEqual(result["spread_j"], value)
                self.assertIn("spread_j", result["failures"])

    def test_degenerate_factor_plane_is_rejected_but_vector_remains_valid(self):
        self.assertEqual(run("degenerate", VectorDirection())["status"], "certified_exact")
        result = run("degenerate", FactorPlaneDirection())
        self.assertEqual(result["status"], "rejected")
        self.assertIn("null_direction", result["failures"])
        self.assertIsNone(result["spread_j"])

    def test_projective_basis_change_and_null_guard(self):
        u, v = (E0, E2), (E1, E3)
        self.assertEqual(spread(u, u), Fraction(0))
        self.assertEqual(spread(u, (plus(E0, E2), E2)), Fraction(0))
        self.assertEqual(spread(u, tuple(reversed(u))), Fraction(0))
        self.assertIsNone(spread((E0, E0), (E1, E3)))
        # Squaring the bilinear pairing loses orientation: opposite rays
        # have zero spread. Do not infer closeness or commutation from it.
        self.assertEqual(spread((E0,), (scaled(-1, E0),)), Fraction(0))
        self.assertEqual(gram(u, u), Fraction(1))

    def test_exact_certificate_replay_and_probability_domain(self):
        a = run("commuting", FactorPlaneDirection())
        b = run("commuting", FactorPlaneDirection())
        self.assertEqual(a, b)
        self.assertEqual(len(a["transcript_sha256"]), 64)
        with self.assertRaises(ValueError):
            schedule_class_mass(a, Fraction(4, 3))

    def test_policy_rejects_negative_thresholds(self):
        with self.assertRaises(ValueError):
            Policy(Fraction(-1), Fraction(0), Fraction(0))


if __name__ == "__main__":
    unittest.main()
