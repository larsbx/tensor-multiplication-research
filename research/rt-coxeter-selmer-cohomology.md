# Exact RT-gated Coxeter route cells and local-to-global audit boundaries

**Status:** mathematical contract + bounded independent F5 reference. Established
results (finite Coxeter relations, cellular boundaries, finite-field Gram
invariance) are distinguished from **proposed** training semantics and
**analogy-only** BSD connections. This note extends
[training-route-audit-experiment](training-route-audit-experiment.md).
Reusable Mojo per-edge gates are proposed in
`larsbx/finite-math-kernels` PR #87, independently of its
permutohedral incidence PR #85 and k-plane spread PR #86.

## 1. RT gate as the local geometric input

Let `F=F_q`, `q` odd, `(V,Q)` a nondegenerate quadratic space and
`B_2(x,y)=Q(x+y)-Q(x)-Q(y)`. For `Q(x)Q(y) != 0` set

```
s([x],[y]) = 1 - B_2(x,y)^2 / (4 Q(x) Q(y)).
D_2(x,y)   = Q(x) Q(y) - (B_2(x,y)/2)^2.
s([x],[y]) = D_2(x,y) / (Q(x) Q(y)).
```

All inverses are guarded. `D_2` is defined even on null inputs, but
the ratio is not. The ratio is invariant under independent rescaling.
For a sigma-semilinear similitude, `s(gx,gy)=sigma(s(x,y))` and a
gate subset `A subset F` must be stable under `sigma` to preserve
admissibility. In F_p sigma is trivial. **Gate membership is a declared
subset test**, not a numeric inequality. Ordinary Cayley–Klein
cross-ratio reconstruction may need a further non-tangency guard;
the Gram ratio is the primary exact kernel.

## 2. Branch B: source-state gated Coxeter 2-faces

Choose `S={0,..,m-1}` of `m<=R` labeled influences, a current ordering
`pi`, and an immutable (for this local *formal* cell) direction
assignment `delta:S -> Ray^x(V,Q)`. For each adjacent transposition
`s_r` define the gate at the **source ordering**

`SG(pi,r)= 1{ s(delta(pi[r]), delta(pi[r+1])) in A }`.

A square has the two paths `s_r s_t` and `s_t s_r` with `t>=r+2`.
A hexagon has paths `s_r s_(r+1) s_r` and
`s_(r+1) s_r s_(r+1)`. The cell exists in the *formal admitted
ordering complex* if **every boundary swap edge** passes at its own
source ordering and its endpoints are present.

```mermaid
flowchart LR
  subgraph Sq["Square: s_r s_t = s_t s_r (|r-t|>1)"]
    P["π"] -->|s_r, gate at π| R["πs_r"]
    P -->|s_t, gate at π| T["πs_t"]
    R -->|s_t, gate at πs_r| Z["πs_rs_t"]
    T -->|s_r, gate at πs_t| Z
  end
  subgraph Hex["Hexagon: s_r s_(r+1) s_r = s_(r+1) s_r s_(r+1)"]
    Q["π"] -->|s_r| A["πs_r"] -->|s_(r+1)| B["πs_rs_(r+1)"] -->|s_r| W["w₀"]
    Q -->|s_(r+1)| C["πs_(r+1)"] -->|s_r| D["πs_(r+1)s_r"] -->|s_(r+1)| W
  end
```

The two paths have the same endpoints by the **symmetric-group Coxeter
relations**, *regardless of spread*. Their signed difference is a
1-cycle. Attaching the corresponding 2-face is a separately gated
decision. The signed boundary is

`partial_2(face) = (sum of path-1 edges) - (sum of path-2 edges)`

and hence `partial_1 partial_2=0` by endpoint cancellation.

**Important:** This is a `S_m` permutation graph, not the Artin braid
group itself: `s_r^2=1` in the symmetric group but not in the braid group.

### Operational effect-equality firewall

For state-dependent tensor operations `U_i`, a geometrically admitted
swap **does not imply** `U_j(U_i(x))=U_i(U_j(x))`. An operational route
cell additionally needs an exact effect-equality certificate at the
*actual execution prefix*, with full optimizer state included. A local
exact swap can then be composed with an identical deterministic suffix.
Null nonzero residuals are never treated as zero. A low-spread or
approximately equal pair can be logged as a *bounded-local candidate*,
not as a homotopy or an equivalence class of executions.

## 3. Bounded computational evidence

`experiments/rt_coxeter_audit_reference.py` implements F5 arithmetic on
the repository's split-eight quadratic form, Coxeter path guards, signed
cell incidence, and deterministic modular ranks. Its six-permutation S3
hexagon has six unique undirected edges. Consequently

```
rank(partial_1)=5,  rank(partial_2)=0 => dim H_1=6-5=1;
rank(partial_1)=5,  rank(partial_2)=1 => dim H_1=6-5-1=0.
```

A separate negative control uses identical non-null direction rays
(spread zero), but a state-dependent update whose two orderings return
different exact vectors. It rejects the inference "spread=0 => equal
computation." The tests do not validate arbitrary training workloads.

For sparse/partial certificate complexes the computed `H_1` is
the homology of the *instantiated* subcomplex, **not automatically** the
homology of the full rank-R abstract complex. Absence of additional
classes requires coverage or a separate global computation.

## 4. Cohomology, admissibility, and the local-to-global comparison

For an admitted finite CW complex `K`, choose bases for `C_j(K;F)`,
and compute `B_j=partial_j`. Then

`H^1(K;F) = ker(B_2^T) / im(B_1^T)`.

The exact dimension certificate is
`dim H^1 = |E| - rank(B_1) - rank(B_2)`.
Each claim must include a boundary-squared check and independent rank
certificates. Dense elimination uses `O(m n min(m,n))` field operations
for an `m x n` matrix; sparsity is an optimization, not an asymptotic
guarantee unless a specific algorithm is analyzed.

**Correction to earlier provisional Selmer notes:** a degreewise
span of "passing" 1-cochains with `C^0_adm=C^0` is **not generally a
cochain subcomplex**: `d^0(C^0)` need not lie in that span. One must
check `d(A^k) subset A^(k+1)` before taking a quotient.

A canonical, well-typed finite comparison instead selects actual
admissible *cellular subcomplexes* `A_alpha subset K` and uses the
restriction cochain maps

`rho:C^*(K;F) -> direct_sum_alpha C^*(A_alpha;F)`.

Form `Sel_RT = Cone(rho)[-1]` with

```
Sel^k = C^k(K) (+) direct_sum C^(k-1)(A_alpha)
D^k  = [ d_K^k        0
         rho^k      -d_A^(k-1) ].
```

This chain map satisfies `D^(k+1)D^k=0` exactly when the restrictions
commute with `d`. Its long exact sequence supplies **distinct**
invariants:

```
Sha_like^ker := ker(H^1(K) -> direct_sum H^1(A_alpha))
Def^k        := coker(H^k(K) -> direct_sum H^k(A_alpha)).
```

These are *named combinatorial analogues*, not the arithmetic
Tate–Shafarevich group. Changing the patch cover can change them.
Overlapping patch descent, if desired, requires a specified Čech
totalization and hypotheses on intersections; a two-patch vertex-star
example does not prove cover independence.

A symmetric nondegenerate edge Gram matrix alone does **not** give
finite-field Hodge decomposition. Any harmonic-regulator construction
must check that every claimed harmonic vector is closed and that the
map from the harmonic space to `H^1` is bijective; equality of their
dimensions alone is insufficient. A determinant over `F_q` also does
not replace the integral height regulator or its torsion corrections.

## 5. Function-field BSD comparison: exactly what transfers

For a smooth projective curve `C/F_q`, function field `K=F_q(C)`,
and an elliptic curve `E/K`, standard local Frobenius factors encode
point counts. The global Hasse–Weil `L(E/K,T)` is a rational function
with coefficients in **characteristic zero** (`Z`/`Q`, or suitable
ell-adic coefficients), not a rational function over `F_q` if one
needs to evaluate at `T=q^(-1)`: in `F_q`, the integer `q` equals
zero and has no inverse.

Function-field BSD relates the algebraic multiplicity of the factor
`(1-qT)` at the central point to Mordell–Weil rank, with an
independently defined leading-term expression involving global and
local arithmetic invariants. This is an **imported conjectural/known-in-
specified-cases theorem package**, not an identity obtained from
Coxeter homology. Nor does a geometric spread identify Frobenius
eigenspaces or arithmetic Selmer groups.

A declaration `L_RT(T;phi)=prod_i det(1-T phi|H^i(Sel_RT))^((-1)^(i+1))`
defines a **family** depending on a genuinely specified chain-map
endomorphism `phi`. It does not, without additional proof, force the
BSD leading coefficient. Even for a unipotent Jordan block, the
multiplicity of eigenvalue 1 is 2 while `dim ker(phi-I)=1`.
The arithmetic comparison is therefore a **research interface**:
local-to-global cochain machinery and exact characteristic-polynomial
certificates share formal tools, but no equivalence is asserted.

## 6. Immediate mathematical and software obligations

1. Integrate source-ordering gate checks (upstream kernel PR #87) with
   **per-prefix effect equality** before admitting operational faces.
2. Keep permutohedral incidence (PR #85) independent of the geometric
   direction rank (k-plane PR #86); a 3-influence hexagon is a 2-cell,
   not a 3-cell.
3. Fix a cover and cochain restriction maps and compute a concrete
   example of a kernel-of-localization obstruction with correct degree
   indexing. Do not reuse a "bad local hexagon" cokernel as Sha.
4. For any leading coefficient claim, supply an **independent**
   arithmetic equality rather than defining one side from the other.
5. Distinguish checked F5 fixtures, Mojo hosted CI results,
   imported theorems, and speculative training/BSD transfer claims.

### References
- Björner & Brenti, *Combinatorics of Coxeter Groups*, 2005 (Coxeter relations).
- Hatcher, *Algebraic Topology*, §2 (cellular boundary and cohomology).
- Ulmer, *Elliptic curves over function fields* (function-field BSD and Tate bridge).
- Repo contracts:
  [split Cayley foundations](split-cayley-rt-foundations.md),
  [higher-rank tensor program](higher-rank-tensor-program.md),
  [training-route audit](training-route-audit-experiment.md).
