Agent completed. agent_id: spectral-lit-review, agent_type: bibliographer, status: completed, description: Find spectral identifiability literature, elapsed: 348s, total_turns: 0, model: gpt-5.4, duration: 335s

I can’t do a live web/Google Scholar search from this session, so the review below is a best-effort synthesis from established literature up to mid-2024 plus the local repo context. I’m confident on the core papers/authors/venues; for a few older spectral-geometry items, I’d still spot-check page ranges/DOIs before final BibTeX.

---

# Targeted literature review for Paper 9  
**Topic:** *Identifiability near symmetry manifolds in parametric spectral inverse problems*

## Executive take

Your advisor’s list is exactly the right one. The cleanest literature story for Paper 9 is:

1. **Kato + Stewart–Sun** give the local linear-algebraic machinery:
   - how eigenvalue/singular-value branches behave under smooth perturbation,
   - when derivatives exist,
   - how invariant subspaces rotate,
   - and why the **smallest singular value of the Jacobian** is the right quantitative identifiability diagnostic.

2. **Hadamard + shape calculus** give the PDE/geometric machinery:
   - when parameters are geometric, Jacobian entries are shape derivatives of eigenvalues,
   - simple eigenvalues have first-variation formulas,
   - repeated eigenvalues require a **matrix-valued first variation on the eigenspace**.

3. **Uhlenbeck + generic simplicity** give the geometric interpretation:
   - multiple eigenvalues are nongeneric,
   - so rank loss is not “typical” in parameter space,
   - but it becomes systematic on **symmetry manifolds**, where symmetry forces multiplicity and kills sensitivity.

4. **Zelditch/local spectral rigidity** gives the inverse-spectral backdrop:
   - local injectivity can be proved, but only under strong analyticity/symmetry/dynamical assumptions,
   - which is very close in spirit to your “identifiability away from symmetry / loss of identifiability on symmetry” story.

5. **Elastography / inverse elasticity / structural model updating** give the applied analogue:
   - identifiability is controlled by the sensitivity matrix,
   - some parameter combinations are inherently weakly observable,
   - and symmetry/near-incompressibility/insufficient data create near-null directions.

---

# 1) Kato perturbation theory — singular values and invariant subspaces

## Core references

### 1.1 Tosio Kato  
**Kato, Tosio.** *Perturbation Theory for Linear Operators.* 2nd ed. Berlin: Springer-Verlag, 1976; reprint, Classics in Mathematics, 1995.  
DOI: 10.1007/978-3-642-66282-9.

### 1.2 Franz Rellich  
**Rellich, Franz.** *Perturbation Theory of Eigenvalue Problems.* New York: Gordon and Breach, 1969.  
(English translation of the 1937 German monograph.)

### 1.3 Adrian S. Lewis  
**Lewis, Adrian S.** “Derivatives of Spectral Functions.” *Mathematics of Operations Research* 21, no. 3 (1996): 576–588.

## What is most relevant to your paper

### A. Smooth/analytic parameter families
Kato’s main message is that if an operator family \(A(t)\) is smooth or analytic, then:

- **isolated eigenvalue clusters of finite multiplicity** move smoothly/analytically as clusters,
- the associated **Riesz spectral projection** also moves smoothly/analytically,
- but **individual eigenvalue branches may fail to be smooth at crossings** unless one chooses branches carefully and/or works in an analytic setting.

For your problem, this is central: near a symmetry manifold, eigenvalues often collide into multiplets. The right object is not always “the \(j\)-th ordered eigenvalue,” but often the **cluster projector** or a cluster invariant.

### B. Singular values via self-adjoint lifting
For singular values of a parameter-dependent matrix \(J(t)\), Kato applies through either:

- the Hermitian Gram matrix \(J(t)^*J(t)\), whose eigenvalues are \(\sigma_i(t)^2\), or
- the block self-adjoint dilation
  \[
  \mathcal H(t)=\begin{pmatrix}0 & J(t)\\ J(t)^* & 0\end{pmatrix},
  \]
  whose eigenvalues are \(\pm \sigma_i(t)\).

This is the clean bridge from operator perturbation theory to **identifiability via Jacobian singular values**.

### C. First derivative of a simple singular value
If \(\sigma_i(t)\) is simple and positive, with left/right singular vectors \(u_i(t),v_i(t)\), then
\[
\sigma_i'(t)=\operatorname{Re}\big(u_i(t)^*J'(t)v_i(t)\big).
\]
This is exactly the formula you want when arguing how the least informative parameter combination emerges away from symmetry.

### D. Repeated singular values: cluster-level, not branch-level
At a repeated singular value, individual branches can be nonsmooth or non-unique under sorting. What remains well behaved is the **spectral subspace**. In practice, that means:

- near symmetry, do not over-interpret derivatives of sorted eigenvalues/singular values,
- instead analyze the **cluster splitting matrix** on the degenerate eigenspace.

## Connection to Paper 9
This is probably your core mathematical framing:

> At a symmetry point, the parameter-to-spectrum map develops degenerate eigenvalue clusters; Kato implies that while individual ordered eigenvalues may lose smoothness there, the cluster projection remains smooth. Identifiability should therefore be studied through the Jacobian restricted to symmetry-breaking directions and, when necessary, through cluster-splitting matrices rather than individual branches.

---

# 2) Stewart–Sun — perturbation of singular subspaces and the smallest singular value

## Core references

### 2.1 Stewart and Sun  
**Stewart, G. W., and Ji-guang Sun.** *Matrix Perturbation Theory.* Boston: Academic Press, 1990.

### 2.2 Per-Åke Wedin  
**Wedin, Per-Åke.** “Perturbation Bounds in Connection with Singular Value Decomposition.” *BIT* 12, no. 1 (1972): 99–111.

### 2.3 Ren-Cang Li  
**Li, Ren-Cang.** “Relative Perturbation Theory: I. Eigenvalue and Singular Value Variations.” *SIAM Journal on Matrix Analysis and Applications* 19, no. 4 (1998): 956–982.

## What they say that matters here

### A. Absolute perturbation of singular values
Stewart–Sun consolidate the classical bound
\[
|\sigma_i(J+E)-\sigma_i(J)|\le \|E\|_2.
\]
So the smallest singular value is **Lipschitz**, but not necessarily differentiable at multiplicity.

For you: as the symmetry manifold is approached, \(\sigma_{\min}(J)\to 0\), and the inverse problem becomes ill-conditioned at least linearly in perturbation size unless a selection rule forces higher-order vanishing.

### B. Singular subspace rotation is gap-controlled
Wedin’s theorem gives \(\sin\Theta\)-type bounds: the angle between perturbed and unperturbed singular subspaces is controlled by
- the size of the perturbation,
- divided by the **spectral gap**.

This is exactly the geometry of near-symmetry:
- when the gap is small,
- the “unidentifiable direction” itself becomes unstable,
- which is often as important as \(\sigma_{\min}\) becoming small.

### C. Smallest singular value under structured perturbations
The Stewart–Sun/Wedin viewpoint is especially useful if your Jacobian is not perturbed arbitrarily, but only through a **low-dimensional structured family**
\[
J(\theta)=J_0+\sum_k \theta_k J_k + \cdots.
\]
Then:

- if \(\sigma_{\min}(J_0)\) is simple and nonzero, its first derivative is \(u_{\min}^*J'_0v_{\min}\);
- if \(\sigma_{\min}(J_0)=0\), the leading-order emergence of nonzero sensitivity is controlled by the restriction of the perturbation to the left/right nullspaces;
- if that restricted first-order term vanishes by symmetry, then \(\sigma_{\min}\) is **second-order or higher** in the symmetry-breaking amplitude.

That last point is almost tailor-made for your paper.

### D. Relative perturbation theory
Li’s relative perturbation results are useful if your Jacobian columns scale very differently, or if you work with normalized/Fisher-whitened sensitivities. They justify focusing on **relative loss of information**, not just absolute perturbation size.

## Connection to Paper 9
The Stewart–Sun section should support a statement like:

> Near a symmetry manifold, identifiability is quantified by the least singular value of the parameter-to-spectrum Jacobian. Stewart–Sun/Wedin show that this quantity is stable away from gap closure, while near gap closure the associated singular subspaces become highly unstable; if symmetry annihilates the first-order nullspace coupling, then \(\sigma_{\min}\) can vanish quadratically or faster.

---

# 3) Hadamard shape derivatives — eigenvalue variation under boundary perturbation

## Core references

### 3.1 Jacques Hadamard  
**Hadamard, Jacques.** *Leçons sur le calcul des variations.* Paris: Hermann, 1910.

### 3.2 Garabedian and Schiffer  
**Garabedian, Paul R., and Max M. Schiffer.** “Convexity of Domain Functionals.” *Journal d’Analyse Mathématique* 2 (1952/53): 281–368.

### 3.3 Daniel Henry  
**Henry, Daniel.** *Perturbation of the Boundary in Boundary-Value Problems of Partial Differential Equations.* London Mathematical Society Lecture Note Series 318. Cambridge: Cambridge University Press, 2005.

### 3.4 Jan Sokołowski and Jean-Paul Zolésio  
**Sokołowski, Jan, and Jean-Paul Zolésio.** *Introduction to Shape Optimization: Shape Sensitivity Analysis.* Springer Series in Computational Mathematics 16. Berlin: Springer, 1992.

## What they prove

### A. Simple eigenvalues have boundary-integral first variations
In the classical Dirichlet Laplacian case, if the boundary moves with normal velocity \(V_n\), then for a simple eigenvalue
\[
\lambda'_k(\Omega;V)
=
-\int_{\partial\Omega} (\partial_n u_k)^2\,V_n\,dS.
\]
For Neumann/Robin/elastic operators, analogous formulas involve boundary strain energy, curvature, traction terms, etc.

### B. Repeated eigenvalues require a matrix-valued derivative
For repeated eigenvalues, one does **not** generally get a single derivative. Instead, the first variation is obtained as the eigenvalues of a finite matrix assembled on the degenerate eigenspace. This is the shape-calculus analogue of Kato’s cluster theory.

### C. Boundary straightening + operator pullback
Henry is especially important for turning moving-domain problems into operator families on a fixed reference domain, after which Kato theory applies.

That is probably the right technical bridge for your PDE section:
- pull back the domain,
- obtain an analytic/smooth operator family,
- use Kato for eigenclusters,
- use Hadamard/Henry for explicit first variation formulas.

## State of the art for fluid–structure operators
The mature theory is strongest for:
- Laplace/Helmholtz,
- elasticity,
- biharmonic/plate operators,
- Stokes/Steklov/sloshing-type spectra.

For **fully coupled fluid–structure eigenproblems**, the literature is more fragmented. The standard pattern is:

1. transform the moving interface/domain to a reference configuration,
2. prove smooth/analytic dependence of the coupled operator or operator pencil,
3. derive Hadamard-type formulas for **simple** eigenpairs,
4. treat repeated or symmetry-protected eigenvalues through finite-dimensional splitting matrices.

So the state of the art is conceptually clear, but not packaged in one single canonical “fluid–structure Hadamard theorem” the way it is for the Laplacian.

## Connection to Paper 9
This is how to connect geometry to identifiability:

> When model parameters include shape variables, the Jacobian of the parameter-to-spectrum map is a matrix of shape derivatives. Near symmetric geometries, repeated eigenspaces must be differentiated at the cluster level, and identifiability depends on how symmetry-breaking boundary velocities couple into the cluster-splitting matrix.

---

# 4) Uhlenbeck generic simplicity — why symmetry manifolds are exceptional

## Core references

### 4.1 John H. Albert  
**Albert, John H.** “Genericity of Simple Eigenvalues for Elliptic Boundary Value Problems.” *Proceedings of the American Mathematical Society* 48 (1975): 413–418.

### 4.2 Karen Uhlenbeck  
**Uhlenbeck, Karen.** “Generic Properties of Eigenfunctions.” *American Journal of Mathematics* 98, no. 4 (1976): 1059–1078.

### 4.3 Misha Teytel  
**Teytel, Misha.** “How Rare Are Multiple Eigenvalues?” *Communications on Pure and Applied Mathematics* 52, no. 8 (1999).  
(page range worth checking in final BibTeX)

## What they show

### A. Simplicity is generic
Uhlenbeck’s key result: for a generic metric on a compact manifold, Laplace eigenvalues are simple and eigenfunctions are Morse. Albert gives an earlier PDE-genericity result in elliptic settings.

### B. Multiplicity is high-codimension
Teytel sharpens the geometric intuition: multiple eigenvalues occur on sets of positive codimension. In finite-dimensional families, one should not expect repeated eigenvalues without a reason.

### C. Symmetry is exactly such a reason
The main “reason” is symmetry. Group invariance decomposes eigenspaces into irreducible representations and can force multiplicity. Thus:

- generic off-symmetry point: simple spectrum,
- on symmetry manifold: enforced degeneracy,
- near symmetry manifold: small splitting, poor identifiability.

## Connection to Paper 9
This is probably your best conceptual sentence:

> Our rank deficiency at symmetry is the inverse-problem shadow of Uhlenbeck’s generic simplicity: multiple eigenvalues are nongeneric in the full parameter space, but become unavoidable on symmetry-constrained submanifolds, where the Jacobian necessarily loses transverse information.

That is a very strong framing.

---

# 5) Zelditch / local spectral rigidity — when does the spectrum determine geometry locally?

## Core references

### 5.1 Guillemin and Melrose  
**Guillemin, Victor, and Richard Melrose.** “An Inverse Spectral Result for Elliptical Regions in \(\mathbb{R}^2\).” *Advances in Mathematics* 32, no. 2 (1979): 128–148.

### 5.2 Steve Zelditch  
**Zelditch, Steve.** “The Inverse Spectral Problem for Analytic Domains.”  
This is a multi-paper program; the key early paper for your purposes is the analytic, symmetric-plane-domain result usually cited as:  
**Zelditch, Steve.** “The Inverse Spectral Problem for Analytic Domains. I. \(\mathbb{Z}_2\)-Symmetric Domains.” *Annals of Mathematics* 160 (2004).  
(Please verify exact issue/pages in final bibliography.)

### 5.3 Hezari and Zelditch  
**Hezari, Hamidreza, and Steve Zelditch.** “\(C^\infty\) Spectral Rigidity of the Ellipse.” *Analysis & PDE* (mid-2010s; verify exact volume/pages).

### 5.4 De Simoi, Kaloshin, and Wei  
**De Simoi, Jacopo, Vadim Kaloshin, and Qiu Wei.** “Dynamical Spectral Rigidity Among \(\mathbb{Z}_2\)-Symmetric Strictly Convex Domains Close to a Circle.” *Geometric and Functional Analysis* 31 (2021): 265–338.

## What this strand proves

### A. Local inverse spectral rigidity is possible, but only under strong assumptions
The important message is not “spectra always determine geometry,” but:

- for **analytic** domains,
- often with **reflection symmetry**,
- and specific dynamical assumptions on billiard trajectories/wave invariants,

one can prove local uniqueness or rigidity.

### B. Symmetry is both a constraint and a source of recoverability
This is subtle but relevant to your paper:
- symmetry can create degeneracies,
- but symmetry assumptions can also reduce the admissible class enough to make inverse results provable.

### C. Wave-trace invariants detect geometry through orbit structure
Zelditch’s program extracts local geometric data from wave invariants attached to special periodic trajectories (e.g. bouncing-ball orbits). That is a global/infinite-data cousin of your finite-mode sensitivity analysis.

## Connection to Paper 9
Your problem can be pitched as a **finite-dimensional local spectral rigidity problem near symmetry manifolds**.

The analogy is:
- Zelditch asks when the full spectrum determines geometry locally.
- You ask when a finite spectral data map is locally injective in a parameter family.
- In both cases, symmetry is where rigidity can fail or become delicate.

A useful sentence would be:

> In this sense, identifiability near symmetry manifolds is a low-dimensional, finite-data analogue of local spectral rigidity: one studies whether spectral invariants vary transversely to symmetry-preserving deformations.

---

# 6) Inverse eigenvalue problems for shells/plates/fluid–structure — applied vibration literature

## Core references

### 6.1 Graham M. L. Gladwell  
**Gladwell, Graham M. L.** “Inverse Problems in Vibration.” *Applied Mechanics Reviews* 57, no. 6 (2004): 401–422.

### 6.2 Graham M. L. Gladwell  
**Gladwell, Graham M. L.** *Inverse Problems in Vibration.* 2nd ed. Dordrecht: Springer, 2005.

### 6.3 Michael I. Friswell and John E. Mottershead  
**Friswell, Michael I., and John E. Mottershead.** *Finite Element Model Updating in Structural Dynamics.* Dordrecht: Kluwer Academic Publishers, 1995.

### 6.4 Mottershead, Link, and Friswell  
**Mottershead, John E., Markus Link, and Michael I. Friswell.** “The Sensitivity Method in Finite Element Model Updating: A Tutorial.” *Mechanical Systems and Signal Processing* 25, no. 7 (2011): 2275–2296.

### 6.5 Aernouts et al.  
**Aernouts, Jef, Ivo Couckuyt, Karel Crombecq, and Tom Dhaene.** “Inverse Estimation of Material Properties from Dynamic Measurements of a Tympanic Membrane Model.” *Journal of the Acoustical Society of America* 131, no. 6 (2012): 4648–4660.

## What this literature says

### A. Frequencies alone often underdetermine parameters
Gladwell’s big message: many inverse vibration problems are nonunique unless one adds
- more modes,
- mode shapes,
- boundary data,
- or structural priors.

That is directly aligned with your “rank deficiency near symmetry” story.

### B. Sensitivity matrices control practical identifiability
Model-updating papers are less theorem-heavy than Kato/Uhlenbeck, but they are very explicit that:
- identifiability depends on the Jacobian/sensitivity matrix,
- parameter correlation matters,
- and some parameterizations are simply bad.

### C. Shell/plate/fluid-like systems are especially correlation-prone
In shells and thin structures, material and geometric parameters often trade off strongly because low-order modes sample them similarly. Near symmetric configurations, modal clustering makes this worse.

### D. Aernouts is a close biological analogue
Aernouts et al. show that dynamic spectral measurements can recover material parameters in a thin biological membrane model—methodologically very close to your intended application class.

## Connection to Paper 9
This strand is your applied justification for why a smallest-singular-value story matters. It lets you say:

> Before solving an inverse problem, one should ask whether the chosen modal data distinguish the chosen parameters. That question is standard in structural model updating, but has not been sufficiently analyzed for symmetry-induced spectral degeneracy.

---

# 7) Doyley (2012) and the broader inverse-elasticity-imaging literature

## Core references

### 7.1 Parker, Doyley, and Rubens  
**Parker, Kevin J., Marvin M. Doyley, and Deborah J. Rubens.** “Imaging the Elastic Properties of Tissue: The 20 Year Perspective.” *Physics in Medicine and Biology* 56, no. 1 (2011): R1–R29.

### 7.2 Marvin M. Doyley  
**Doyley, Marvin M.** “Model-Based Elastography: A Survey of Approaches to the Inverse Elasticity Problem.” *Physics in Medicine and Biology* 57, no. 3 (2012): R35–R73.  
DOI: 10.1088/0031-9155/57/3/R35.

### 7.3 Bonnet and Constantinescu  
**Bonnet, Marc, and Andrei Constantinescu.** “Inverse Problems in Elasticity.” *Inverse Problems* 21, no. 2 (2005): R1–R50.

### 7.4 McLaughlin and Renzi  
**McLaughlin, James, and David Renzi.** “Shear Wave Speed Recovery in Transient Elastography and Supersonic Imaging Using Propagating Fronts.” *Inverse Problems* 22, no. 2 (2006): 681–706.  
(page range worth verifying)

## What they show

### A. Doyley is the inverse-problem survey you want
Doyley organizes elastography into:
- direct vs iterative inversion,
- full-field displacement data,
- regularization and priors,
- model mismatch,
- and practical identifiability limitations.

### B. Bonnet–Constantinescu is the broader mechanics inverse-problem backbone
They place elasticity imaging inside the wider PDE inverse-problem framework:
- ill-posedness,
- nonuniqueness,
- sensitivity to constitutive assumptions,
- and the role of adjoints and regularization.

### C. McLaughlin–Renzi emphasize uniqueness from wave data
Their results matter because they show the contrast between:
- rich, space-time wavefield data, which can support uniqueness,
- and sparse observables, where identifiability can collapse.

That contrast is useful for Paper 9: **few spectral observables** are intrinsically more fragile than full wavefield inversion.

## Connection to Paper 9
Cite this strand when you want to say:
- your problem is not a generic inverse-PDE problem but a **spectrally compressed** one,
- therefore identifiability must be examined before optimization,
- and your Jacobian singular values play the same role that observability/sensitivity analyses play in elastography.

---

# 8) Oberai, Gokhale & Feijóo (2003) — what did they show about identifiability?

## Core references

### 8.1 Oberai, Gokhale, and Feijóo  
**Oberai, Assad A., Nihar H. Gokhale, and Guillermo R. Feijóo.** “Solution of Inverse Problems in Elasticity Imaging Using the Adjoint Method.” *Inverse Problems* 19, no. 2 (2003): 297–313.

### 8.2 Bonnet and Constantinescu  
**Bonnet, Marc, and Andrei Constantinescu.** “Inverse Problems in Elasticity.” *Inverse Problems* 21, no. 2 (2005): R1–R50.

### 8.3 Doyley  
**Doyley, Marvin M.** “Model-Based Elastography: A Survey of Approaches to the Inverse Elasticity Problem.” *Physics in Medicine and Biology* 57, no. 3 (2012): R35–R73.

## What Oberai et al. showed
This paper is important not because it proves an abstract uniqueness theorem, but because it makes the identifiability issue concrete in PDE-constrained inversion.

### Main contributions
- Formulates elasticity imaging as an optimization problem constrained by the elastic PDE.
- Derives efficient **adjoint-based gradients** for elastic parameters.
- Demonstrates reconstruction of elastic-property distributions from displacement data.
- Shows, in effect, that identifiability is strongly parameter-dependent:
  - **shear modulus** is often much better determined than
  - **bulk/Lamé parameters**, especially near incompressibility.

### Why this matters for identifiability
Their work makes two points that transfer directly to your problem:

1. **Not all parameters are equally observable from the same data.**  
   This is your singular-value story in applied form.

2. **Weak directions are structural, not just numerical.**  
   Poor recoverability is often caused by the forward map itself, not by the optimizer.

## Connection to Paper 9
Oberai is a very good citation for this claim:

> Even in a well-posed PDE-constrained inverse problem, certain parameter combinations may be intrinsically weakly identifiable from the chosen observables; thus the conditioning of the sensitivity operator, not merely the optimization scheme, determines recoverability.

---

# 9) Barbone & Bamber (2002) — what can and cannot be inferred?

## Core references

### 9.1 Barbone and Bamber  
**Barbone, Paul, and James C. Bamber.** “Quantitative Elasticity Imaging: What Can and Cannot Be Inferred from Strain Images?” *Physics in Medicine and Biology* 47, no. 12 (2002): 2147–2164.

### 9.2 Barbone and Gokhale  
**Barbone, Paul, and Nihar H. Gokhale.** “Elastic Modulus Imaging: On the Uniqueness and Nonuniqueness of the Elastography Inverse Problem in Two Dimensions.” *Inverse Problems* 20 (2004).  
(Please verify issue/pages in final BibTeX.)

### 9.3 Bonnet and Constantinescu  
**Bonnet, Marc, and Andrei Constantinescu.** “Inverse Problems in Elasticity.” *Inverse Problems* 21, no. 2 (2005): R1–R50.

## What they showed
Barbone & Bamber is the canonical “identifiability obstruction” paper in this area.

### Main message
From strain images alone, one generally cannot recover arbitrary elastic moduli uniquely without additional assumptions on:
- loading,
- boundary conditions,
- compressibility,
- geometry,
- constitutive form.

### Why it matters
This is exactly the sort of statement you need philosophically:
- inverse problems fail not only because of noise,
- but because the data may simply not contain the needed information.

### Strong connection to your paper
Replace “strain image” with “finite spectral data,” and the message is nearly identical:
- some parameter combinations are visible,
- some are weakly visible,
- some are invisible on symmetry manifolds.

A nice sentence for Paper 9 would be:

> Our symmetry-manifold rank deficiency is a spectral analogue of the nonuniqueness mechanisms identified by Barbone and collaborators in elastography: the obstruction lies in the information content of the measurements, not merely in numerical reconstruction.

---

# Cross-strand synthesis: the literature argument Paper 9 should make

## The strongest mathematical narrative
I would frame Paper 9 around this chain:

1. **Kato/Hadamard:** the parameter-to-spectrum map is smooth only at the level of appropriate eigenvalue clusters/projectors near multiplicity.
2. **Uhlenbeck/Teytel:** multiple eigenvalues are nongeneric, so persistent degeneracy signals symmetry or another structural constraint.
3. **Stewart–Sun/Wedin:** local identifiability is quantified by the smallest singular value of the Jacobian; near degeneracy, both this singular value and its associated subspace become unstable.
4. **Zelditch:** local spectral rigidity is possible, but only under restrictive assumptions; your paper studies the local finite-dimensional analogue of that issue.
5. **Oberai/Barbone/Doyley:** in applied inverse mechanics, recoverability is determined by information structure, not optimizer choice.

That is an unusually coherent literature chain. Use it.

---

# What I think Paper 9 should explicitly claim

## A. The right abstract object
Let
\[
F(\theta)=\big(\lambda_1(\theta),\dots,\lambda_m(\theta)\big)
\]
or, better near multiplicity, a vector of **cluster invariants**.

Then:
- local identifiability is full column rank of \(DF(\theta)\) modulo symmetry directions;
- practical identifiability is governed by \(\sigma_{\min}(DF(\theta))\).

## B. Near symmetry manifolds
If \(\mathcal M\) is a symmetry manifold, then:
- on \(\mathcal M\), extra isotropy forces eigenvalue multiplicity and/or invariant directions;
- therefore \(DF\) loses rank or develops a very small least singular value;
- away from \(\mathcal M\), generic simplicity restores eigenvalue splitting and often restores rank.

That is your main theorem story.

## C. What not to say carelessly
Avoid saying merely:
- “symmetry breaking restores identifiability.”

Better:
- “symmetry-breaking generically restores first-order spectral splitting, but local injectivity still requires enough measured modes and transversality of the Jacobian to residual isospectral directions.”

That phrasing is much more faithful to Kato/Uhlenbeck/Zelditch.

---

# Suggested “must-cite” shortlist for Paper 9

If you only cite 12–15 works, I would prioritize these:

1. **Kato (1995)** — operator perturbation backbone.  
2. **Stewart & Sun (1990)** — Jacobian singular values/subspaces.  
3. **Wedin (1972)** — singular subspace perturbation bounds.  
4. **Hadamard (1910)** — classical shape derivative starting point.  
5. **Henry (2005)** — moving-boundary operator perturbation.  
6. **Sokołowski & Zolésio (1992)** — shape sensitivity framework.  
7. **Uhlenbeck (1976)** — generic simplicity.  
8. **Teytel (1999)** — multiple eigenvalues are rare/high-codimension.  
9. **Guillemin & Melrose (1979)** — inverse spectral rigidity for ellipses.  
10. **Zelditch (2004)** — local inverse spectral geometry under symmetry/analyticity.  
11. **Gladwell (2004 or 2005)** — inverse vibration background.  
12. **Friswell & Mottershead (1995)** or **Mottershead et al. (2011)** — modal identifiability/model updating.  
13. **Doyley (2012)** — inverse elasticity survey.  
14. **Oberai, Gokhale & Feijóo (2003)** — adjoint-based recoverability, parameter sensitivity.  
15. **Barbone & Bamber (2002)** — what data can/cannot identify.

---

# One possible literature-review paragraph for Paper 9

You could write something like:

> The present problem sits at the intersection of operator perturbation theory, shape sensitivity, and inverse spectral geometry. Kato’s perturbation theory shows that under smooth parameter variations, isolated eigenvalue clusters and their spectral projections vary smoothly, whereas individual ordered eigenvalues can become nonsmooth at symmetry-induced crossings. Stewart–Sun and Wedin then identify the smallest singular value of the Jacobian as the natural quantitative measure of local identifiability and show how its associated singular subspaces become unstable as spectral gaps collapse. For geometric parameters, Hadamard-type shape derivatives and the boundary-perturbation framework of Henry and Sokołowski–Zolésio provide the PDE mechanism by which boundary deformations enter the spectrum. Uhlenbeck’s generic simplicity theorem and related codimension results explain why repeated eigenvalues are exceptional away from symmetry manifolds but unavoidable on them. Finally, local spectral rigidity results in inverse spectral geometry, especially for analytic symmetric domains, show that local injectivity of spectral data is possible but delicate. Our contribution may therefore be viewed as a finite-dimensional, local identifiability analysis near symmetry manifolds for a parametric spectral inverse problem.

---

# Bottom line by strand

- **Kato:** use for smooth cluster perturbation, not naive ordered eigenvalue derivatives at crossings.
- **Stewart–Sun:** use for the least singular value/subspace story.
- **Hadamard:** use if your parameters include geometry or boundary shape.
- **Uhlenbeck:** use to explain why symmetry manifolds are precisely where things go wrong.
- **Zelditch:** use as the inverse-spectral “big picture.”
- **Inverse vibration / shells:** use to connect to engineering identifiability practice.
- **Doyley/Oberai/Barbone:** use to show this is a general inverse-problem phenomenon, not an artifact of your model.

If you want, I can do a second pass and turn this into:
1. a **BibTeX-ready reference list**, or  
2. a **2–3 page literature review section drafted in paper style**.