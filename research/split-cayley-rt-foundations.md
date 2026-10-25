# Split Cayley rational trigonometry: corrected foundations and tensor reconstruction

**Status:** research note; established algebraic identities are distinguished from proposed extensions. All scalar inversions are guarded; no real, complex, or analytic substrate is required.

## 1. Quadratic substrate

Let `F` be a field with `char(F) != 2`; let `(V,N)` be a nondegenerate quadratic space, and put

\[
B(x,y)=\tfrac12\big(N(x+y)-N(x)-N(y)\big).
\]

For affine vectors `x,y`, quadrance is `Q(x,y)=N(y-x)` (total). For projective non-null rays define

\[
s([x],[y])=1-\frac{B(x,y)^2}{N(x)N(y)},\quad N(x)N(y)\ne0.
\]

**Polynomial kernel:** `N(x)N(y)(1-s)=B(x,y)^2`, with the same nonzero guard. Multiplying denominators is an equivalence only on the guarded locus. Scaling representatives preserves `s`.

Reflections in `a` with `N(a) != 0` have the explicit form

\[
r_a(x)=x-2\frac{B(x,a)}{N(a)}a.
\]

If `N(x)=N(y)=a != 0`, one reflection `r_(x-y)` sends `x` to `y` when `N(x-y) != 0`. Otherwise `N(x+y)=4a != 0` and `r_y r_(x+y)` sends `x` to `y`. This is a **deterministic, two-reflection** transport argument, with no intermediate-vector search.

## 2. Corrected Zorn split Cayley product

Write `X=(α,a;b,β)` with `α,β ∈ F`, `a,b ∈ F³`. Define

\[
\begin{aligned}
(\alpha,a;b,\beta)(\gamma,c;d,\delta)
=(&\alpha\gamma+a\cdot d,\\
&\alpha c+\delta a+b\times d;\\
&\gamma b+\beta d-a\times c,\\
&\beta\delta+b\cdot c).
\end{aligned}
\]

**The minus sign on the lower cross product is essential** with this orientation convention. Use

\[
N(X)=\alpha\beta-a\cdot b,\qquad \bar X=(\beta,-a;-b,\alpha).
\]

The unit is `(1,0;0,1)`; direct coefficient expansion proves `N(XY)=N(X)N(Y)` and `X X̄=X̄ X=N(X)1`. Inversion is defined iff `N(X) != 0`, via `X̄ / N(X)`. The split algebra is alternative, and the Moufang identities and Artin's two-generated associativity theorem follow from the standard alternative-algebra results. Do **not** use the false identity `[x,y,z]x=[x,y,zx]`; it fails even in split Cayley algebras.

## 3. Higher-rank correction to triple spread

For three non-null vectors `x,y,z`, let

\[
u=N(x),\ v=N(y),\ w=N(z),\quad
a=B(x,y),\ b=B(y,z),\ c=B(z,x),\quad K=uvw.
\]

Their pair spreads are `s₁=1-a²/(uv)`, `s₂=1-b²/(vw)`, `s₃=1-c²/(wu)`. Set

\[
D_\pm=K\pm 2abc-wa^2-ub^2-vc^2.
\]

Exact rational algebra gives the **triple-spread defect**

\[
\boxed{(s_1+s_2+s_3)^2-2(s_1^2+s_2^2+s_3^2)-4s_1s_2s_3
=-\frac{D_+D_-}{K^2}.}
\]

`D₊` is the three-vector Gram determinant. The classical zero-defect triple-spread theorem applies to a two-dimensional span because then `D₊=0`. It is **not true for arbitrary triples in dimension >=3**. Conversely, a zero defect can arise via `D₋=0` even when the Gram matrix is nonsingular.

## 4. Seven-dimensional trace-zero tensor reconstruction

The trace-zero subspace `W={x:B(x,1)=0}` has dimension seven and `C(F)=F1 ⊕ W`. For `u,v ∈ W` set

\[
u\times v=\tfrac12(uv-vu),\qquad
\varphi(u,v,w)=B(u\times v,w).
\]

Then `φ ∈ Λ³W*` is alternating, and multiplication decomposes as

\[
uv=-B(u,v)1+u\times v.
\]

More generally

\[
(a,u)(b,v)=(ab-B(u,v),\;av+bu+u\times v).
\]

Because `B` is nondegenerate, `(B,φ)` reconstructs the cross product and the multiplication **when compatibility conditions for a Cayley tensor package hold**. An arbitrary symmetric form plus arbitrary three-form is not automatically Cayley multiplication.

Exact identities include

\[
N(u\times v)=N(u)N(v)-B(u,v)^2,\qquad
B(u\times v,u)=B(u\times v,v)=0,
\]

and for the associator `A(u,v,w)=(uv)w-u(vw)`,

\[
\boxed{N(A(u,v,w))=4\big(\det\operatorname{Gram}_B(u,v,w)-\varphi(u,v,w)^2\big).}
\]

A zero associator norm does **not** imply a zero associator in split geometry. The three-form formula yields a guarded projective invariant on triples with nonzero Gram determinant, but no implication of associativity is asserted from its scalar value.

## 5. Rational orthogonal operators

For `u ∈ W`, let `K_u(v)=u×v`. The exact operator reduction is

\[
K_u^2(v)=B(u,v)u-N(u)v,\quad K_u^3=-N(u)K_u.
\]

`K_u` is skew-adjoint with respect to `B`. For `d=1+t²N(u) != 0`, the Cayley transform

\[
R_{u,t}=(I-tK_u)(I+tK_u)^{-1}
=I-\frac{2t}{d}K_u+\frac{2t^2}{d}K_u^2
\]

preserves `B`, with polynomial kernel `d R=d I-2tK_u+2t²K_u²`. **It need not preserve multiplication or φ**, so it need not belong to `G₂(F)`.

In arbitrary dimension, any skew-adjoint `K` permits the guarded transform `R_K(t)=(I-tK)(I+tK)^{-1}` when `det(I+tK) != 0`. This is an orthogonal construction independent of composition algebras.

## 6. Provenance and claims

The Zorn construction, Artin/Moufang laws, and `G₂` symmetry are established mathematics. The novelty target here is a computationally disciplined synthesis: polynomial certificates, guarded rational invariants, higher-frame Gram corrections, and minimal tensor packages. No new classification theorem, cryptographic hardness claim, universal speedup, or original proof of Artin/Moufang is asserted.

Reproduce coefficient identities using `python tests/split_cayley_tensor_certificate.py` (requires `sympy`). Sampling, where used, is only a regression aid.

**References:** R. D. Schafer, *An Introduction to Nonassociative Algebras* (1966); T. A. Springer and F. D. Veldkamp, *Octonions, Jordan Algebras and Exceptional Groups* (2000); N. J. Wildberger, *Divine Proportions* (2005).
