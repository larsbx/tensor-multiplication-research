# Research experiment: parameterized tensor directions for training-route audits

**Status:** exploratory exact-rational reference and negative controls; not an LLM training guarantee or a proof that approximate diamonds are homotopies.

## Repository placement and division of responsibility

This experiment belongs in **tensor-multiplication-research**: it uses the existing exact quadratic/spread and higher-rank tensor framework to ask whether local training-update reorderings admit independently auditable certificates. The **finite-math-kernels** repository is the canonical location for reusable Mojo arithmetic and Gram/exterior kernels, not for a speculative training auditor. **finite-swarm-dynamics** is a potential downstream consumer, not the authoritative home for this tensor-interface experiment.

## A finite exact model

The ambient space is `V=Q^4`, viewed as a flattened 2x2 tensor. The bilinear form is the rational dot product `B(u,v)=sum_i u_i v_i` and the quadrance is `N(u)=B(u,u)`. The toy update `U_i` is specified by **two factors whose sum is its displacement**. All arithmetic is `fractions.Fraction`; no floating point, limits, root extraction, or unguarded division are used.

For an update step `s` there are two independently selectable direction adapters:

- **Vector:** `dir(s)=(s.target-s.source,)`, rank 1.
- **Factor plane:** `dir(s)=(f1,f2)`, rank 2, **only if** the two recorded factors sum to the exact displacement. Rank deficiency is deliberately visible.

For direction bases `U=(u_1,...,u_r)`, `V=(v_1,...,v_r)`, set `G(U,V)=(B(u_a,v_b))`. Define

```text
norm_r(U)   := det G(U,U)
pair_r(U,V) := det G(U,V)
s_r(U,V)    := 1 - pair_r(U,V)^2/(norm_r(U)*norm_r(V))
domain      := norm_r(U)*norm_r(V) != 0
kernel      := norm_r(U)*norm_r(V)*(1-s_r) == pair_r(U,V)^2
```

Basis changes by invertible `r x r` matrices cancel in the ratio. Rank 1 is the ordinary projective spread. Rank 2 is the exterior/Grassmann version; it measures alignment of **spans**, not magnitudes or final parameter equality.

**Guards:** null/degenerate Gram determinants are rejected, never silently interpreted as spread zero. The calculation is exact in `Q`, where an ordering supports nonnegative threshold comparisons. It is **not** claimed that the same `<=` policy works in `F_p`; finite-field variants must use an explicit acceptance subset or other domain-specific predicate.

## Correct local swap contract

For exact update functions `U_i,U_j:V->V` and anchor `A`:

```text
B := U_i(A)                    C := U_j(A)
D_ij := U_j(B)                 D_ji := U_i(C)
i_before := B-A               i_after := D_ji-C
j_before := C-A               j_after := D_ij-B
```

The experiment checks all four edge quadrances, both guarded direction spreads, and the **independent endpoint quadrance** `N(D_ij-D_ji)`.

Verdicts are deliberately distinct:

- `certified_exact`: all policy checks pass **and** `D_ij == D_ji`. This is an actual 2-cell for the local path presentation.
- `bounded_local_only`: guarded checks pass with nonidentical endpoints whose exact squared discrepancy is within the declared rational bound. **No topological 2-cell and no global route-equivalence assertion.**
- `rejected`: at least one policy/guard fails. Failure reasons remain explicit.

The geometric predicate cannot establish computational equivalence on its own. Squaring the pairing loses orientation, so opposite vectors also have zero spread. Neither equal spans nor small spread implies small endpoint error, optimizer-state equivalence, or preserved training behavior.

## Probability and deterministic auditing

For a toy schedule distribution `P(ij)=2/3`, `P(ji)=1/3`, the program combines masses **only when the two schedules are exactly related by the certified 2-cell**. Otherwise it keeps two distinct classes, even if the bounded-local predicate passes. This separates probability **over routes** from deterministic replay of a particular pair of routes.

Each record stores exact fractions, endpoints, guards, failure reasons, and a canonical SHA-256 transcript digest. The digest identifies record content; it does not authenticate the update implementation. Validation requires pinned source code, replay of both update functions, exact evaluation of guards, and comparison against the independently recomputed record. A hash alone is not a proof.

## Initial scenarios and falsification tests

| Scenario | Vector direction | Factor-plane direction | Main question |
| --- | --- | --- | --- |
| Commuting additive updates | exact | exact | Does a true commuting diamond pass both adapters? |
| Rescaled second update | bounded local | bounded local | Can spread pass even though the endpoints differ? **Yes**. |
| Tilted second update | rejected on spread | rejected on spread | Does each adapter detect a controlled direction change? |
| Dependent recorded factors | exact | rejected as degenerate | Does a rank-2 guard catch the information loss that rank 1 misses? |

The vector and factor-plane adapters deliberately disagree on the numerical spread of the rescaled update (`1/26` versus `0`). That is not an inconsistency: they audit different geometric objects. This is why the interface is parameterized rather than assuming one tensor-direction interpretation.

## Reproducibility

```sh
python -m unittest discover -s tests -p 'test_training_route_audit.py' -v
python experiments/training_route_audit.py
```

No external dependency is needed for this experiment. The existing SymPy coefficient certificate remains separate and authoritative for split-Cayley polynomial identities.

## Mathematical and implementation obligations before using LLM traces

1. **State completeness:** an optimizer update depends on moments, learning-rate schedule, RNG, and possibly distributed state. The full audit state must include those, not just a flattened weight vector.
2. **Replay fidelity:** verify deterministic execution or record exact update effects; arbitrary float-to-rational conversion checks only a declared projection, not the native floating computation.
3. **Global error composition:** a sequence of bounded-local diamonds does not automatically imply a bounded final difference. Supply an explicit propagated-error rule or rerun both complete routes.
4. **Rank-lift correctness:** require full rank and correct factor provenance for every chosen adapter. Compare modes and record null cases rather than inventing a preferred interpretation.
5. **Finite probability:** schedule probabilities are rational and sum to one; probabilistic schedule selection is distinct from exact certificate checking.
6. **Higher coherence:** three-way braid/commutation coherence requires separately verified faces and boundary data. Pairwise approximate diamonds alone do not imply a 3-cell.
7. **Kernel reuse:** once mathematics and interface are accepted, port `Gram`, exact rational/exterior spread, and canonical witnesses to `finite-math-kernels` as an independently tested Mojo consumer, not as a wholesale speculative migration.

**Research hypothesis:** a configurable exterior-spread adapter may help identify training-step reorderings with low directional change, while a separate endpoint guard prevents false claims of exact commutation. Performance on real, instrumented LLM training traces remains completely untested.
