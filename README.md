# Tensor Multiplication Research

Finite-field tensor geometry, rational trigonometry, structured bilinear multiplication, and higher-rank algebraic invariants.

## Current research notes

- [Split Cayley RT: corrected foundational identities](research/split-cayley-rt-foundations.md) — Zorn multiplication and norm, projective guards, triple-spread defect, trace-zero three-form reconstruction, associators, and rational orthogonal operators.
- [Higher-rank tensor research program](research/higher-rank-tensor-program.md) — minimal tensor packages, Aschbacher questions, semilinear covariance, exact structured weights and verification gates.
- [Exact polynomial certificate](tests/split_cayley_tensor_certificate.py) — runnable symbolic checks over ℤ[1/2].

- [Parameterizable tensor-direction training-route audit experiment](research/training-route-audit-experiment.md) — exact-rational vector and factor-plane adapters, guarded diamonds, negative controls, and deterministic replay records.

- [RT-gated Coxeter and cohomology boundary](research/rt-coxeter-selmer-cohomology.md) — explicit source-ordering gates, square/hexagon cellular homology, Selmer comparison typing and finite-field BSD caveats; independent F5 reference + tests.

## Verification

Requires Python 3.10+ and SymPy. Run:

```sh
python -m pip install 'sympy>=1.12,<2'
python tests/split_cayley_tensor_certificate.py
python -m unittest discover -s tests -p 'test_rt_coxeter_reference.py' -v
```

The certificate checks polynomial **coefficient identities** rather than sampling a small finite field. Equalities over ℤ[1/2] transfer to any field of odd characteristic. A green workflow is a checked computation, not a substitute for proving separate imported Artin/Moufang classification results.

## Research standard

Every claim must be tagged as established, derived with an explicit proof or certificate, or conjectural. Prefer exact polynomial identities, explicit denominator guards, and small reproducible tests. Do not assume that zero norm implies zero vector in a split space. Do not identify an arbitrary tensor stabilizer with an Aschbacher class without checking the ambient classical group and classification hypotheses. Any performance or cryptographic claims require separate evidence.
