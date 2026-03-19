# Born Rule Derivation via Coalgebraic Path Integral

> Session 2026-03-17c. Status: route identified, test cases verified, formal proof outstanding.

## Summary

A specific derivation route for the Born rule (|psi|^2 probability measure) from OCT's coalgebraic foundations. The argument chain connects the Mealy machine functor, complex signal space, enriched category theory, and the Feynman path integral. Each step is either established mathematics or a checkable structural correspondence.

If this argument holds under formal scrutiny, it resolves O6, O13, and O14 simultaneously — they are one question, not three.

---

## The Argument Chain

### Step 1: Node as Mealy machine (established)

Every node is a coalgebra for the Mealy machine functor F_Sigma(S) = Sigma x (Sigma -> S), where Sigma is a parameter (signal space) that varies by grain.

A coalgebra is a set S (state space) with a map alpha: S -> Sigma x (Sigma -> S), decomposing into:
- output: S -> Sigma (current state produces an output signal)
- transition: S x Sigma -> S (current state + input signal -> new state)

### Step 2: Iteration as path

A node starts in state s_0. It receives a sequence of signals sigma_1, sigma_2, ..., sigma_n from Sigma. Each signal transitions the state:

s_1 = t(s_0, sigma_1), s_2 = t(s_1, sigma_2), ..., s_n = t(s_{n-1}, sigma_n)

Each sequence of signals is a path through state space. Different signal sequences = different paths.

### Step 3: At quantum grain, Sigma = complex phase space (boundary-tested)

Signals at quantum grain are complex phases. The photon IS the phase pattern — strip the phase and nothing remains. Massive particles (nodes) inherit phase from constitution at this grain.

Boundary tests passed (Session 2026-03-17c):
- Electron phase: inherited from constitution at phase-Sigma grain
- Higgs mechanism: constitution event; photons unaffected (no Higgs input channel for photons)
- Pair production: bidirectional constitution (signal -> node, node -> signal); taxonomy holds at any moment

### Step 4: Complex Sigma forces C-enriched category structure (checkable)

If Sigma is a complex vector space and transitions are complex-linear (the superposition principle — not an additional assumption, but what "Sigma is complex" means for the dynamics), then:

- State spaces S are complex vector spaces
- Structure-preserving maps between coalgebras (hom-sets) are linear maps between complex vector spaces
- Linear maps between complex vector spaces form a complex vector space
- Composition of linear maps is bilinear

Therefore Coalg(F_Sigma) is naturally C-enriched when Sigma is a complex vector space with linear transitions. This is checkable against standard enriched category theory.

### Step 5: Enriched colimits produce complex-weighted path sums (established math)

In a C-enriched category, colimits are coends — weighted colimits that produce complex-weighted sums over diagram morphism chains. This is established enriched category theory (reference: Kelly, "Basic Concepts of Enriched Category Theory").

The colimit of a diagram in C-enriched Coalg(F_Sigma) sums over all morphism chains (paths), weighted by their complex values (phases).

### Step 6: This IS the Feynman path integral (structural correspondence)

The correspondence:

| Feynman Path Integral | OCT Coalgebraic Colimit |
|---|---|
| Path x(t) from a to b | Signal sequence (morphism chain) in diagram |
| Action S[x] | Accumulated phase along morphism chain |
| Phase weight e^(iS/hbar) | Complex Sigma-value of the morphism chain |
| Sum over paths integral Dx(t) | Colimit over all morphism chains |
| Propagator K(b,a) | Colimit value |
| \|K\|^2 = probability | Sustainability measure |

The iterated Mealy machine, summed over all signal paths via C-enriched colimit, IS the path integral in discrete form. The continuous limit is a standard mathematical procedure.

### Step 7: Path integral = Hilbert space QM (established, Feynman 1948)

The path integral formulation and the Hilbert space formulation of quantum mechanics are mathematically equivalent. This was established by Feynman and is standard physics.

### Step 8: Hilbert space + Gleason = Born rule (established, Gleason 1957)

Gleason's theorem: given a Hilbert space of dimension >= 3, the only consistent probability measure is the Born rule |psi|^2. The "squaring" is not arbitrary — it is the unique consistent transition from phase-space to probability-space.

### Step 9: Connection to sustainability criterion

The Born rule |A|^2 IS the sustainability measure at quantum grain:
- Phase destruction (lossy integration) produces magnitude
- |A|^2 > 0: valid colimit, new node forms
- |A|^2 = 0: no valid colimit, no new node
- The sustainability criterion applied at a grain where Sigma IS phase naturally produces |psi|^2

---

## Why Sigma Must Be Complex (O13/O14 connection)

### The Argument from Perspectivalism (Session 2026-03-18 — strengthened)

The U(1) requirement is derived from OCT's own commitments, not imported:

1. **"Signal IS phase"** (settled Session 2026-03-17c) — at quantum grain, signals are phase patterns. Strip the phase from a photon and nothing remains.
2. **Phase has no absolute reference** — mathematical fact about angles. An angle is defined relative to a reference direction; without one, it has no value.
3. **OCT perspectivalism** — no node has privileged status; constitution events are perspectival.
4. **Perspectivalism extends to signals** — signals are relational entities (they exist between nodes, not absolutely). At quantum grain where signal = phase, the phase of a signal is only defined relative to the receiving node's current state. No node's "zero" is more real than any other's.
5. **Therefore**: changing which node's reference direction defines "zero" — rotating all phases by the same angle — cannot change any physical outcome.
6. **The group of "change phase reference" transformations** = {multiply all signals by e^(i*theta)} = U(1), by definition.
7. **Therefore**: sustainability criterion is U(1)-invariant.

This forces Sigma to support U(1) action. The minimal signal space with U(1) symmetry is C (complex numbers). Real numbers have no rotation symmetry — only +1 and -1.

### The Chain

- O14 (framework symmetry = perspectivalism) forces U(1) at quantum grain
- U(1) forces complex Sigma (O13)
- Complex Sigma forces C-enriched colimits = path integral
- Path integral forces Hilbert space
- Hilbert space + Gleason forces Born rule (O6)

Three open unknowns, one answer.

### Generalization to Other Gauge Groups

The perspectivalism argument is not specific to U(1). At each grain, the gauge group is determined by the structure of Sigma:

- Electromagnetic Sigma (phase on a circle, 1D) → U(1)
- Weak force Sigma (2D phase structure) → SU(2)
- Strong force Sigma (3D "color" structure) → SU(3)
- Gravitational Sigma → diffeomorphism invariance (= general relativity)

One principle (perspectivalism), different Sigma at each grain, different gauge groups. All gauge symmetries in physics as consequences of OCT perspectivalism.

**Scope boundary:** This argument produces continuous gauge symmetries. Discrete symmetries (parity, charge conjugation, time reversal) are not addressed. The weak force's parity violation is not explained by this argument.

### Previous Weakest Link — Status

The U(1) step was identified as the weakest link. The perspectivalism argument grounds it in OCT's own commitments rather than asserting it. Each step is either an OCT commitment (perspectivalism, signal IS phase), a mathematical fact (phase requires reference, U(1) is the rotation group), or established physics. No external import required.

**Remaining formal work:** Verify that the argument from perspectivalism to U(1) can be stated as a mathematical theorem (not just a conceptual argument). The conceptual case is strong; the formal statement is outstanding.

---

## Verification Against Known Physics

### Double-slit experiment

**Setup:** Source S, two slits, detector position D. Two paths with phases phi_1, phi_2.

**OCT prediction:**
- Colimit at D: A(D) = e^(i*phi_1) + e^(i*phi_2)
- Sustainability measure: |A(D)|^2 = |e^(i*phi_1) + e^(i*phi_2)|^2
- Paths differ by integer wavelengths: constructive -> bright fringe -> node forms
- Paths differ by half-wavelength: destructive -> dark fringe -> no node

**QM prediction:** Identical. **Experiment:** Matches.

### Which-path information

**Setup:** Detector placed at Slit_1.

**OCT prediction:** Detector constitutes new node at Slit_1. Signal consumed. New signal emitted. Only one path to D. No sum. No interference.

**QM prediction:** Identical. **Experiment:** Matches.

### Three-slit / Sorkin test (higher-order interference)

**Setup:** Three slits with phases phi_1, phi_2, phi_3.

**OCT prediction:** A(D) = e^(i*phi_1) + e^(i*phi_2) + e^(i*phi_3). |A|^2 decomposes into individual + pairwise terms. NO three-way or higher terms. No higher-order interference.

**QM prediction:** Identical (Born rule is quadratic). **Experiment:** Confirmed to high precision.

**Significance:** The framework's structure (linear phase sum, quadratic sustainability measure) automatically forbids higher-order interference without additional postulates.

### Entanglement / Bell correlations

**Setup:** Entangled photon pair. Alice measures at angle alpha, Bob at angle beta.

**OCT prediction:**
- Entangled pair = one colimit at quantum grain
- Colimit state = singlet state (1/sqrt(2))(|up-down> - |down-up>)
- Measurement fragments colimit; fragments inherit colimit structure
- Correlation: E(alpha, beta) = -cos(2(alpha - beta))
- CHSH violation: 2*sqrt(2) (Tsirelson bound)

**QM prediction:** Identical. **Experiment:** Matches.

**Tsirelson bound explanation:** The bound is 2*sqrt(2) (not 4) because C-enriched colimits produce Hilbert space, and Hilbert space's inner product structure constrains maximum correlation. A different Sigma would produce a different bound.

### Classical limit

**The quantum/classical boundary dissolves as a folk category.**

- Quantum grain: Sigma = complex phase space. C-enriched colimits. Interference, superposition, entanglement.
- Higher grains (atomic, molecular, cellular): Sigma = electromagnetic, chemical, electrical. Signals don't carry raw quantum phase. C-enrichment dilutes.
- Classical dynamics = what OCT produces when Sigma is no longer purely phase-based.

Decoherence is not something that "happens to" quantum systems — it IS grain transition. The classical world is the same framework with different Sigma.

---

## What This Is NOT

- **Not just relabeling QM.** The Tsirelson bound explanation, classical limit as grain transition, and Born rule derivation from sustainability criterion are explanatory additions, not renaming.
- **Not a proven theorem.** The argument is at "route identified, test cases pass" stage. Formal verification by someone with expertise in enriched category theory + path integral mathematics is required.
- **Not claiming to replace QM.** QM's mathematical apparatus is correct. OCT provides a framework within which QM's postulates become theorems — if the argument holds.

## What Would Falsify This

- C-enriched colimits in Coalg(F_Sigma) do NOT produce linear phase sums (checkable math — would break Step 5)
- Higher-order interference is found experimentally (would break both QM and OCT)
- The sustainability measure turns out to be something other than |A|^2 (would break the Gleason connection)
- The U(1) symmetry argument for complex Sigma fails — sustainability criterion doesn't require phase-rotation invariance (would break O13/O14 connection but not the rest of the chain if complex Sigma is accepted empirically)

---

## Status of Open Unknowns

| Unknown | Status |
|---|---|
| O6 (Born rule) | Route identified. Derivation chain laid out. Pending formal verification. |
| O13 (Sigma at quantum grain) | Answered: complex phase space. Boundary-tested. |
| O14 (Framework symmetry) | Identified as U(1)/phase-rotation invariance of sustainability criterion. Weakest link — needs stronger justification. |
| O16 (Why this probability?) | Resolved IF O6 holds: Born rule = Gleason on Hilbert space from C-enriched colimit. |

## Key Insight

The Mealy machine iterated over signal sequences IS a discrete path integral. This is not analogy. It is structural identity. The path integral was discovered by Feynman as a computational technique; in OCT, it emerges as the natural colimit construction at any grain where Sigma is complex.

---

## Next Steps

1. **Formal verification:** Check that Coalg(F_Sigma) with complex Sigma and linear transitions is C-enriched, and that enriched colimits produce the claimed path sums. This is specific enough for a mathematician to evaluate.
2. **U(1) justification:** Strengthen the argument for why sustainability criterion requires phase-rotation invariance. This is the weakest link.
3. **Continuous limit:** Verify that the discrete-to-continuous limit of the coalgebraic path sum recovers the standard Feynman path integral measure.
4. **Expert review:** This argument sits at the intersection of coalgebra theory, enriched category theory, and quantum foundations. Finding a reviewer with expertise in all three is the critical next step.
