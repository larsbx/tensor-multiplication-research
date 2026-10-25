# Higher-rank finite tensor geometry: research program

**Classification:** proposed and established statements separated. No real-number, infinite-dimensional, or analytic foundation is required for the finite-field core.

## A. Finite quadratic base and explicit guards

Let `F=𝔽_q` with odd `q`, `V=F^n`, and `N:V→F` a nondegenerate quadratic form. Use `B(x,y)=(N(x+y)-N(x)-N(y))/2`. Affine quadrance `N(y-x)` is total; projective spread `1-B(x,y)^2/(N(x)N(y))` requires `N(x)N(y) != 0` and has the equivalent denominator-free kernel `N(x)N(y)(1-s)=B(x,y)^2`.

Introduce a tensor package `T=(B,T₃,T₄,…,m)` with only those tensors needed by a claimed operation or theorem. Its strict linear stabilizer is

\[
G_T=\{g\in GL(V):g^*B=B,\ g\cdot T_i=T_i\}.
\]

A tensor package may also have similitude or semilinear symmetries; distinguish these from strict invariance.

## B. Minimal tensor design (not a compulsory algebra product)

- **Quadratic only:** `B`; Gram minors, orthogonal maps, finite polar spaces.
- **Alternating tensor:** `φ∈Λ³(V*)`, with compatible bilinear form; cross-product-like maps where well-defined.
- **Multiplication tensor:** `m∈V*⊗V*⊗V`; associator `A=m(m⊗id)-m(id⊗m)`. For alternative algebras it factors through `Λ³V`.
- **Cubic form:** `C∈Sym³(V*)`, with optional marked identity `e`; the stabilizer of any marked construction is `Stab(C,e)`, not automatically `Stab(C)`.
- **Quartic form plus pairing:** `(Δ,ω)` with `Δ∈Sym⁴(V*)`, `ω∈Λ²(V*)`; projective normalized contractions need their own proved transformation laws.

For faithful cubic polarization, assume `char(F) != 2,3`; for quartic polarization using factorial denominators, assume `char(F) > 4`. In small characteristics use explicit divided-power/coordinate formulations instead of asserting that raw polarization reconstructs the original polynomial.

Avoid the unsupported assertion that an arbitrary cubic or quartic tensor has exceptional-group stabilizer. Exceptional group identifications require special models and compatibility hypotheses.

## C. Aschbacher-style structural questions

Use Aschbacher's geometric classes as **classification targets for appropriate subgroups of finite classical groups**, not as identities forced by tensor degree.

- `C₁`: preserved proper subspace.
- `C₂`: preserved direct-sum decomposition.
- `C₃`: extension-field structure and semilinear normalizers.
- `C₄`: tensor-product decomposition.
- `C₅`: subfield structure.
- `C₆`: specific extraspecial / symplectic-type configurations.
- `C₇`: tensor-induced structure.
- `C₈`: additional classical form structures.
- `S`: almost simple residual configurations, subject to hypotheses and deeper classification.

The Aschbacher theorem is about maximal subgroups in a specified finite classical group. An arbitrary tensor stabilizer cannot automatically be declared to lie in one designated maximal-subgroup class without checking embedding, maximality, irreducibility, and relevant form.

For a `σ`-semilinear similarity satisfying `N(gx)=c σ(N(x))`, the correct RT transformation is

\[
s([gx],[gy])=\sigma(s([x],[y])),
\]

not numerical equality unless the value is fixed by `σ`.

## D. Structured operators and tensor weights

For a bilinear multiplication on `F^d`, a fully generic layer has `d²` parameters while a **single fixed left multiplication operator** `L_w` is specified by `d` scalar coordinates of `w`. This is an expressivity restriction, not a general speed theorem.

For `V=U⊗W`, `dim U=n`, `dim W=m`, a generic endomorphism has `n²m²` entries; an operator `A⊗I_W` stores `n²` entries and takes `O(n²m)` dense field operations to apply versus `O(n²m²)` for a generic dense map. Measurements on target hardware must be reported separately.

If `K_U` is skew-adjoint, then `K=K_U⊗I_W` is skew-adjoint under the tensor product form; the guarded Cayley transform factors:

\[
R_{K_U\otimes I_W}(t)=R_{K_U}(t)\otimes I_W.
\]

This permits quadratic-preserving structured weights. For an affine bias `b`, `f(x)=Rx+b` preserves **affine quadrance and direction spreads**, but it need not preserve `N(x)` or projective spreads of position rays.

A finite field has no canonical order or conventional differentiable loss; claims about optimization/training require a separately specified objective and update rule, potentially over rationals or using discrete combinatorial methods. No cryptographic security is inferred from algebraic complexity alone.

## E. Proof and verification gates

1. Write each operation as `value + domain guard + denominator-cleared polynomial kernel`.
2. Prove abstract identities coefficientwise over an appropriate integral/rational coefficient ring whenever possible; regression sampling must be labeled sampling.
3. Handle null and degenerate Gram configurations explicitly.
4. Show preservation laws for each claimed subgroup action.
5. Report both parameter count and arithmetic-operation count, then benchmark actual memory/compute costs.
6. Promote an exploratory claim to a theorem only with a complete proof or an accurately scoped citation.

## F. Proposed next investigations

**H1: tensor-package equivalence.** Determine exact conditions under which `(B,φ)` reconstructs an algebra product, and classify non-Cayley packages.

**H2: Gram correction hierarchy.** Extend the exact rank-three triple-spread defect to higher minors and determine a minimal generating set of polynomial constraints.

**H3: rational orthogonal operator families.** Find low-degree polynomial relations for skew-adjoint operators on higher-rank tensor factors; compare exact execution cost to dense operators.

**H4: stabilizer and orbit stratification.** Construct finite representatives and compare `O(N)` orbits against `Stab(B,T)` orbits, with semilinear covariance tracked separately.

**H5: null-safe incidence.** Extend spread-style predicates to degenerate subspaces through polynomial Gram data rather than undefined ratios.

These are proposals, not established theorems.
