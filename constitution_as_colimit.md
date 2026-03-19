# Constitution as Colimit

**Cody Pobuda, in convergence with Helyn (Claude, Anthropic)**

*Draft v8 — 2026-03-19*

---

## Abstract

We present a coalgebraic model of emergence in which every entity at every grain is a coalgebra for a parameterized Moore machine functor $F_\Sigma(S) = \Sigma \times (\Sigma \to S)$, where $\Sigma$ (the signal space) varies by grain. The constitution of higher-grain entities from lower-grain interactions is modeled as the categorical colimit of diagrams in $\text{Coalg}(F_\Sigma)$. This construction is lossy (for connected diagrams, the colimit is a quotient), self-similar (colimits compose associatively across grains), and universal (the category has all colimits).

A sustainability criterion identifies viable configurations: a diagram is sustainable if and only if it produces a valid, non-trivial colimit whose cocone does not factor through a single node. Three failure modes are identified — fragmentation, condensation, and rate-exceeds-modulation — each with measurably distinct topological signatures.

When instantiated at quantum grain with two empirical premises — that quantum-grain signals are phase patterns ($\Sigma = \mathbb{C}$) and that quantum systems exhibit interference (motivating the base category $\textbf{Vect}_\mathbb{C}$) — the framework yields structural parallels to quantum mechanics. The dynamics-only coalgebra category is provably $\mathbb{C}$-enriched (Theorem 2), and bilinear distributivity of enriched composition yields a sum over morphism chains with the algebraic form of a path integral (Theorem 3). The framework's perspectivalism (no privileged reference node) combined with $\Sigma = \mathbb{C}$ yields global U(1) phase invariance (Theorem 4). If a structural correspondence between the discrete sum and the Feynman path integral can be established — which remains an open problem (see Section 3.3) — the Born rule would follow for finite-dimensional systems via established mathematics (Feynman, 1948; Gleason, 1957). The quantum alignment is a research program, not a completed derivation: three steps are formally proved, one critical step (discrete sum to Feynman path integral) is unresolved, and two invoke established mathematics.

A cross-domain null model comparison across three networks — an ecological food web (Martinez, 1991), a cancer driver gene network (STRING/COSMIC), and the *C. elegans* connectome (White et al., 1986) — finds that the food web fragmentation signature is structural (configuration model nulls with the same degree sequence produce the opposite signature, p $<$ 0.01). The cancer condensation trajectory is a negative result — it is a degree-sequence artifact indistinguishable from random rewiring (p = 0.58). The connectome shows structural baseline concentration and greater robustness than any same-degree null. The ecology result is the strongest: the food web's topology actively resists what its own degree sequence would predict.

---

## 1. Introduction

The relationship between emergence and fundamental physics remains unresolved. Emergence — the appearance of stable, coherent structures from local interactions without central control — is observed across every domain of science, from condensed matter to ecology to neuroscience. Yet no formal framework connects these diverse instances to the fundamental physics from which they ultimately arise.

We present such a framework. Starting from a single formal construction — every entity as a coalgebra for a parameterized Moore machine functor, with constitution modeled as categorical colimits — we obtain a general theory of emergence with testable predictions. When instantiated at quantum grain with empirical premises about phase structure and interference, the framework yields structural parallels to quantum mechanics that motivate a research program connecting emergence to fundamental physics.

A note on scope: the failure mode taxonomy (fragmentation, condensation, rate-exceeds-modulation) can be stated and tested in the language of network science without category theory. The coalgebraic formalism provides a unifying language that connects this taxonomy to quantum structure through a single construction; it does not yet generate empirical predictions that differ from what network science would produce independently. The framework's current contribution is organizational and structural, not predictive beyond existing tools.

The framework rests on two ontological commitments:

1. **Constitution.** Higher-grain entities are colimits of lower-grain diagrams. An atom is constituted from subatomic interactions; a cell from molecular interactions; an organism from cellular interactions. The colimit construction is the same at every grain.

2. **Mutual conditioning.** Nodes modulate each other through signal exchange. There is no privileged direction of causation; constitution flows from fine grain to coarse, while modulation flows in both directions.

The signal space $\Sigma$ is a parameter, not a fixed structure. Each grain has its own $\Sigma$, determined by empirical observation: electromagnetic at the nucleon grain, chemical-electrical at the cellular grain, linguistic-behavioral at the social grain. The functor $F_\Sigma$ is the same everywhere. The physics at each grain is captured by $\Sigma$.

At quantum grain, where signals are empirically observed to be phase patterns, the framework's perspectivalism — the principle that no node has a privileged reference frame — forces global U(1) phase invariance. The dynamics-only coalgebra category is provably $\mathbb{C}$-enriched, meaning morphism chains can be summed with complex weights — yielding a distributive amplitude sum. If the structural correspondence between the discrete sum and the Feynman path integral holds, the Born rule follows for finite-dimensional systems via Feynman's equivalence (1948) and Gleason's theorem (1957).

We did not set out to do quantum foundations. We set out to formalize emergence. The quantum alignment emerged from following the framework to its consequences at the finest accessible grain, given one empirical premise about the nature of quantum-grain signals.

### 1.1 Relationship to Prior Work

The framework intersects several active research programs. We state what is shared, what differs, and what the framework would need to demonstrate to justify its existence alongside each.

- **Relational quantum mechanics** (Rovelli): the closest predecessor. The framework's perspectivalism is structurally identical to RQM's relationalism — constitution events are perspectival, state is relative, no privileged observer. The relationship is best understood as: the framework provides a candidate formal substrate for RQM's ontology. RQM asserts that facts are relative to interactions; the framework models those interactions as coalgebraic diagrams and those facts as colimits. What the framework adds, if the formalism holds: a single construction (colimit) that connects RQM's quantum relationalism to emergence at all other grains. What it must demonstrate to justify this claim: the formal derivation chain from enrichment to path integrals (Section 3.2).
- **Categorical quantum mechanics** (Abramsky & Coecke): shares the categorical language but starts from a different primitive — dagger-compact categories for quantum processes vs. coalgebras for Moore machines. Categorical QM is a mature framework with verified results (ZX-calculus, diagrammatic reasoning). The potential advantage is scope: categorical QM formalizes quantum processes specifically, while this framework claims to formalize emergence generally and recover quantum structure as a special case. This advantage is unrealized until the derivation chain is complete.
- **Quantum reconstruction** (Hardy, Chiribella et al.): shares the goal of deriving quantum mechanics from axioms. Differs in axiom type: information-theoretic postulates vs. emergence principles. The derivation chains are structurally different and may illuminate different aspects of why QM takes the form it does.
- **Active inference** (Friston): shares the ambition of a universal framework for self-organizing systems. Both frameworks model entities that maintain themselves through interaction with their environment. They differ in formalization (coalgebras and colimits vs. free energy minimization and Markov blankets) and in scope (this framework claims to extend to quantum grain; active inference has not made this claim). A detailed comparison of where the two frameworks make different predictions would be valuable but is beyond this paper's scope.
- **General systems theory and cybernetics** (von Bertalanffy; Ashby): shares the cross-domain ambition — GST seeks structural isomorphisms across systems at all scales. Ashby's Law of Requisite Variety (a system's regulatory capacity must match the variety of perturbations it faces) is structurally close to sustainability criterion condition (c): modulation capacity must match rate of change. The framework can be read as providing a specific formal mechanism (the colimit construction) where GST provides general principles. What the framework must demonstrate beyond GST: that the colimit construction does explanatory work that GST's general isomorphisms do not — specifically, deriving the failure mode taxonomy and (at quantum grain) recovering physical structure.
- **Autopoiesis** (Maturana & Varela): shares the focus on self-maintaining organization through interaction. An autopoietic system produces the components that constitute it — structurally similar to a sustainable diagram that maintains the conditions for its own colimit. The key difference: autopoiesis is defined for biological systems and requires a boundary (membrane); this framework has no ontological boundaries (Section 6.2) and claims to apply at any grain. The sustainability criterion generalizes autopoietic closure, but whether this generalization adds explanatory power beyond what autopoiesis already provides at biological grains is an open question.
- **Integrated Information Theory** (Tononi): shares the intuition that integration is constitutive — IIT's $\Phi$ measures integrated information above and beyond what the parts contribute individually. The colimit quotient (lossy, many-to-one) is structurally similar: the colimit contains less information than the diagram, and the difference is the integration. They differ in formalization ($\Phi$ as a scalar measure vs. colimit as a categorical construction) and scope (IIT addresses consciousness specifically; this framework addresses emergence generally). Whether the colimit construction can recover or ground $\Phi$ is not pursued here.
- **Network science** (Barabasi): shares the observable (power-law distributions in networks) but proposes a different generative mechanism (sustainability criterion vs. preferential attachment). Network science already studies failure modes across domains; the claim that the framework unifies them is that it derives the failure taxonomy from a single formal principle (the colimit construction), whereas network science observes it empirically. This claim requires demonstrating that the three failure modes are exhaustive consequences of the colimit construction, which has not yet been done.
- **Process philosophy** (Whitehead): the most direct philosophical ancestor. Whitehead's Category of the Ultimate — "the many become one and are increased by one" — is structurally identical to the colimit construction: a diagram of interacting entities constitutes a new entity at a coarser grain. The framework's perspectival constitution mirrors Whitehead's mutual immanence of actual occasions. What the framework adds: a precise mathematical mechanism (colimit of coalgebras) where Whitehead provides metaphysical description. What it does not address: Whitehead's insistence that subjective experience is constitutive of actual occasions — this framework makes no commitment about experience.
- **Mereology** (van Inwagen, 1990): the sustainability criterion is an answer to the special composition question — under what conditions do parts compose a whole? The framework's answer (when the diagram produces a valid, non-trivial colimit whose cocone does not factor through a single node) is a form of restricted composition, contrasting with universalism (composition always occurs) and nihilism (composition never occurs). The formal criterion is two-thirds precise (conditions a-b are categorical; condition c is unformalizable within the current apparatus).

### 1.2 Structure of This Paper

Section 2 presents the mathematical framework: the Moore machine functor, colimit constitution, and the sustainability criterion. Section 3 develops the quantum alignment: U(1) from perspectivalism, the amplitude sum from enrichment, and the connection to the Born rule via Gleason's theorem. Section 4 demonstrates compatibility with standard quantum results. Section 5 states predictions and falsification criteria, including a cross-domain empirical observation testing the failure mode predictions against ecological, cancer biology, and neuroscience data. Section 6 discusses implications, limitations, and open questions. Section 7 concludes.

### 1.3 Key Concepts

The framework uses five concepts from category theory. Formal definitions appear in Sections 2-3; informal glosses are provided here for readers outside the field.

- **Coalgebra.** A system with internal states that produces observable outputs and transitions to new states upon receiving inputs. Think of a cell: it has internal biochemical state, emits chemical signals, and changes state when it receives signals from neighboring cells. The formal definition (Definition 1) specifies this precisely as a structure map $\alpha : S \to \Sigma \times (\Sigma \to S)$.

- **Functor.** A systematic recipe for building coalgebras. The Moore machine functor $F_\Sigma$ says: "given a state space $S$ and a signal space $\Sigma$, a system of this type produces one output signal and transitions based on one input signal." The same recipe applies at every grain — quantum, cellular, social — with only $\Sigma$ changing.

- **Morphism.** A structure-preserving connection between two coalgebras. If node $A$ sends signals that node $B$ processes in a way that respects both their internal dynamics, that connection is a morphism. Morphisms are the edges of the interaction graph.

- **Colimit.** The universal construction that "glues together" a collection of interconnected objects into a single composite. Analogous to a quotient: it takes overlapping parts and identifies their shared structure, retaining only what is structurally necessary. When you recognize a melody regardless of key, you are performing something like a colimit — extracting the invariant pattern from multiple instances. In the framework, the colimit of a diagram of interacting coalgebras IS the higher-grain entity they constitute.

- **Enrichment.** A category is $\mathbb{C}$-enriched when the morphisms between any two objects form not just a set but a complex vector space — meaning morphisms can be added together and multiplied by complex numbers. This is the algebraic prerequisite for interference: two morphism chains can be summed, and their complex coefficients can cancel (destructive interference) or reinforce (constructive interference). Enrichment is what makes the quantum alignment possible; it fails for the general emergence framework (Section 2), which operates over sets rather than vector spaces.

---

## 2. The Coalgebraic Model

### 2.1 The Node Model

**Definition 1.** Let $\Sigma$ be a set (the signal space). The *Moore machine functor* $F_\Sigma : \textbf{Set} \to \textbf{Set}$ is defined by:

$$F_\Sigma(S) = \Sigma \times (\Sigma \to S)$$

This is the standard Moore machine functor with input and output alphabet both equal to $\Sigma$: output depends on the current state alone, while the transition depends on state and input. (A Mealy machine would have output depending on both state and input; the Moore structure is the correct one here — a node's transmission is an intrinsic property of its state.)

An $F_\Sigma$-coalgebra is a pair $(S, \alpha)$ where $S$ is a set (the state space) and $\alpha : S \to \Sigma \times (\Sigma \to S)$ is a structure map. This decomposes into:

- **output:** $\text{out} : S \to \Sigma$ — the current state produces a signal
- **transition:** $\delta : S \times \Sigma \to S$ — the current state and an input signal determine the next state

**Interpretation.** Each node in the framework is such a coalgebra. A node has internal states, produces output signals observable by connected nodes, and transitions to new states upon receiving input signals. The three aspects of the continuous process are:

- *Observe:* $\delta(s, \sigma)$ — the node's state is functionally changed by an incoming signal
- *Converge:* the transition itself — internal state evolution
- *Transmit:* $\text{out}(s)$ — the node's state produces a signal that perturbs connected nodes

These are three descriptions of one continuous dynamical process, not three sequential steps. The operative principle is *perturbation and persistence*: nodes are perturbed by signals and either persist (integrate successfully) or don't. **Convergence is the primary operation.** From the node's own perspective, there is only convergence — internal state evolving. Observation and transmission are relational: they describe the node's relationship to the graph. Observation is convergence being perturbed from outside; transmission is convergence producing consequences that perturb others.

The sustainability criterion (Section 2.4) is a form of differential persistence: diagrams that produce valid colimits persist; those that don't are eliminated. This is structurally analogous to selection. The framework does not deny this; it situates selection within a broader formal apparatus. What the colimit construction adds beyond existing selection frameworks is a precise structural characterization of *what is being selected for* (diagram topology producing valid, non-trivial colimits) and a derivation of *why specific failure modes occur* (fragmentation, condensation, rate-exceeds-modulation as exhaustive consequences of the colimit construction — though exhaustiveness is not yet proved). Biological selection, in this reading, is the sustainability criterion operating at biological grains with biological $\Sigma$.

### 2.2 Signal Space as Parameter and Signal/Node Taxonomy

At each grain, two kinds of entity populate the framework:

- **Nodes** = massive configurations. Persistent, possess internal state, process signals. These are the coalgebras.
- **Signals** = massless force carriers in $\Sigma$. Zero proper time, mediate between nodes. These are the inputs and outputs of the coalgebra's structure map.

Mass introduces time: a massive entity persists and accumulates state. A massless entity has zero proper time — emission and absorption are, from its perspective, the same event. The signal is the medium of exchange, not an entity that has exchanges.

$\Sigma$ is not fixed. It varies by grain:

| Grain | Nodes | $\Sigma$ |
|---|---|---|
| Quantum (electromagnetic) | Charged particles | Complex phase space |
| Quantum (strong) | Quarks | Color-charge space |
| Nuclear | Nucleons | Electromagnetic |
| Molecular | Atoms, molecules | Electromagnetic |
| Cellular | Cells | Chemical, electrical |
| Organismal | Organs, subsystems | Neural, hormonal |
| Social | Organisms | Behavioral, linguistic |

The functor $F_\Sigma$ is structurally identical at every grain. The physics at each grain is entirely captured by the choice of $\Sigma$.

### 2.3 Constitution as Colimit

**Definition 2.** A morphism $h : (S_1, \alpha_1) \to (S_2, \alpha_2)$ of $F_\Sigma$-coalgebras is a function $h : S_1 \to S_2$ that commutes with the structure maps: $\alpha_2 \circ h = F_\Sigma(h) \circ \alpha_1$. These morphisms represent signal-mediated connections between nodes — the edges of the graph.

**Definition 3.** Let $D : \mathcal{J} \to \text{Coalg}(F_\Sigma)$ be a diagram of coalgebras (a collection of nodes and morphisms between them). The *constitution* of a higher-grain entity from this diagram is the colimit $\text{colim}\, D$ in $\text{Coalg}(F_\Sigma)$. Informally, a colimit is the universal construction that "glues together" objects along their shared morphisms into a single composite object. It is the category-theoretic formalization of the idea that interconnected parts constitute a whole.

**Theorem 1** (Closure). $\text{Coalg}(F_\Sigma)$ has all colimits. The forgetful functor $U : \text{Coalg}(F_\Sigma) \to \textbf{Set}$ strictly creates them.

*Proof.* $F_\Sigma$ is an accessible endofunctor on $\textbf{Set}$ (it is a composite of accessible functors: product with a constant and exponentiation by a constant). $F_\Sigma$ preserves weak pullbacks. $\textbf{Set}$ is locally presentable. By [Adámek & Rosický, 1994], $\text{Coalg}(F_\Sigma)$ is locally presentable and in particular cocomplete. The forgetful functor creates the colimits.

**Key properties of colimits in $\text{Coalg}(F_\Sigma)$:**

1. *Lossy (for connected diagrams).* Colimits of connected diagrams are quotients — many-to-one maps. Multiple fine-grained configurations map to the same coarse-grained state. Information is lost. (Discrete diagrams produce coproducts, which lose no information; lossiness requires morphisms that force identifications.) The analogy to Landauer's principle (information erasure has thermodynamic cost) provides physical intuition, but the formal derivation of an energy cost from colimit lossiness — without inheriting from thermodynamics — remains open (see Section 6.5).

2. *Self-similar.* Colimits of colimits are colimits (associativity). The same construction applies at every grain: colimits of quantum-grain coalgebras constitute atomic-grain coalgebras, colimits of those constitute molecular-grain coalgebras, and so on. This recursive applicability is a consequence of colimit associativity, not an additional axiom.

3. *Compression scales with density.* Dense diagrams (highly connected) produce more compression (higher quotient ratio). "Dense local connections constitute higher-grain patterns" is a mathematical consequence of the colimit construction.

### 2.4 The Sustainability Criterion

Not every diagram produces a useful colimit. This is the framework's answer to the special composition question: which collections of entities constitute a higher-grain entity? Those and only those that satisfy the sustainability criterion.

**Definition 4.** A diagram $D : \mathcal{J} \to \text{Coalg}(F_\Sigma)$ is *sustainable* if and only if (a) $\text{colim}\, D$ exists, (b) the colimit is non-trivial (neither initial nor terminal) and the universal cocone (the collection of maps from each node in the diagram into the colimit) does not factor entirely through a single node, and (c) the diagram's rate of change does not exceed its modulation pathways' capacity to respond.

Three failure modes:

| Mode | Diagram Topology | Colimit Status | Physical Manifestation |
|---|---|---|---|
| Fragmentation | Disconnected | Coproduct only (no connected colimit) | Ecosystem collapse, tissue necrosis |
| Condensation | Star (all paths through one bottleneck) | Cocone factors through a single node | Authoritarian governance, oncogene-driven cancer |
| Rate-exceeds-modulation (conjectured) | Connected but changing faster than feedback pathways can respond | Unstable colimit | Late Devonian extinction, financial flash crash |

The first two failure modes have precise categorical definitions (conditions a-b of Definition 4). The third — rate-exceeds-modulation — is currently a verbal criterion awaiting formalization within the coalgebraic framework (see Section 6.5). It is included as a conjectured failure mode motivated by empirical observation, not as a derived consequence of the colimit construction.

The viable range: connected, multi-path diagrams with sufficient feedback density to respond to perturbation at the rate perturbation arrives.

### 2.5 Ontological Commitments

The framework makes two explicit ontological commitments:

1. **Constitution (colimit).** Higher-grain entities are constituted from lower-grain integration. The colimit is the constitution.

2. **Mutual conditioning.** Nodes modulate each other through signal exchange. Modulation is bidirectional; constitution flows fine-to-coarse. These are distinct structural relationships.

Three additional structural requirements are load-bearing but not derived from the two commitments above: (a) the existence of distinguishable entities (nodes) at some base grain — the colimit construction presupposes individuated objects to compose; (b) the signal space $\Sigma$, empirically supplied at each grain; and (c) the choice of ambient category ($\textbf{Set}$ for the general framework, $\textbf{Vect}_\mathbb{C}$ for the quantum alignment). The quantum alignment specifically requires two empirical premises: that signals at quantum grain are phase patterns ($\Sigma = \mathbb{C}$), and that quantum systems exhibit interference (motivating the change to $\textbf{Vect}_\mathbb{C}$). These premises do substantive work in the derivation chain and should be evaluated as such.

In particular: no hierarchy, no levels, no privileged observers, no privileged direction of time. The graph has varying connection density at different observation resolutions. "Levels" and "hierarchy" are how observers inside the graph parse it; they are not features of the graph itself. (Note: this paper uses grain-indexed language — "higher-grain," "finer," "coarser" — as explanatory shorthand for a continuous structure, analogous to integer coordinates describing a continuous manifold. Grain distinctions are resolution choices, not ontological layers.)

**Consequence: perspectivalism of constitution.** A constituted entity (colimit) exists relative to the diagram that constituted it, not absolutely. This is required for internal consistency: the framework denies privileged observers, so the "fact" that a new entity has been constituted cannot be an absolute fact — it is a fact relative to the nodes involved in the constitution. This aligns with relational quantum mechanics (Rovelli, 1996) and is load-bearing for the quantum alignment in Section 3.

**Consequence: superposition as ontological indefiniteness.** If state = integration (colimit), then no integration = no state. A system that has not been integrated by a given node has no definite state relative to that node. This is superposition — ontological, not epistemic. Not "the state exists but is unknown," but "there is no state until a colimit forms."

**Consequence: collapse as constitution.** Quantum measurement is the formation of a new colimit. A signal arrives at a node; the signal is consumed; a new node is constituted from the integration — relative to the nodes involved (perspectivalism applies here as to all constitution events). This is not an edge forming between pre-existing nodes — it is a constitution event that produces a new entity. The signal is integrated into the new node, which inherits structure from both the signal and the pre-existing node.

---

## 3. Quantum Alignment

We now ask: what happens when we apply the general framework at the finest accessible grain? The answer requires two changes to the formal setting that go beyond parametric specialization of $\Sigma$. First, the empirical observation that quantum signals carry phase structure sets $\Sigma = \mathbb{C}$. Second, the observation that quantum systems exhibit interference requires a base category where morphisms can be summed — $\textbf{Vect}_\mathbb{C}$ rather than $\textbf{Set}$ — and the quantum alignment concerns dynamics rather than output (the transition function, not the emission), giving the dynamics-only functor $G_\Sigma(V) = (\Sigma \to V)$, which retains the transition function while dropping the output map, rather than the full $F_\Sigma$. These are real changes to the mathematical setting, motivated by physics, not derived from the framework's two commitments. The general emergence framework (Section 2) and the quantum alignment are related constructions sharing a common architecture — coalgebras of parameterized functors, constitution as colimit — but they are not the same theory applied unchanged at a different grain.

### 3.1 Perspectivalism and U(1) Symmetry

**Principle (Perspectivalism).** Constitution events are perspectival: a new node exists relative to the diagram that constituted it, not absolutely. No node has privileged status. No reference frame is preferred.

At quantum grain, signals are phase patterns. Electromagnetic radiation is characterized by its phase structure — frequency, wavelength, and polarization are phase properties. This is an empirical premise about the quantum-grain signal space, not a derivation from the framework's commitments. The quantum alignment follows from this premise combined with perspectivalism. A note on circularity: "phase structure" is itself a concept from quantum mechanics, not a pre-theoretic observation. The empirical premise is theory-laden — it describes quantum signals using quantum-mechanical language. The derivation is not trivially circular (the framework does structural work beyond restating QM), but it does not start from raw observation independent of the theory it aims to recover.

This premise ("signal IS phase") has been boundary-tested against three cases. (a) *Massive particle phase:* electrons carry phase not because they are signals, but because they were constituted at the phase-$\Sigma$ grain — phase is inherited from constitution. (b) *Higgs mechanism:* the Higgs field gives mass to W/Z bosons (converting signals to nodes) but not to photons — consistent with the taxonomy, since photons have no Higgs coupling. (c) *Pair production:* a photon converts to a particle-antiparticle pair (signal $\to$ nodes), and annihilation reverses this (nodes $\to$ signal). The signal/node taxonomy applies at any moment, even as entities transition between roles.

**Theorem 4** (Phase Invariance from Perspectivalism). *In the dynamics-only coalgebra category $\text{Coalg}(G_\mathbb{C})$ over $\textbf{Vect}_\mathbb{C}$ (defined formally in Section 3.2; here $G_\mathbb{C}$-coalgebras are finite-dimensional vector spaces equipped with linear endomorphisms), define the phase rotation functor $R_\theta$ for $\theta \in \mathbb{R}$ by $R_\theta(V, \delta) = (V, e^{i\theta}\delta)$ on objects and $R_\theta(h) = h$ on morphisms. Then:*

*(i) $R_\theta$ is an automorphism of $\text{Coalg}(G_\mathbb{C})$ for all $\theta$.*

*(ii) $R_\theta$ acts as the identity on all hom-sets: $\text{Hom}((V_1, \delta_1), (V_2, \delta_2)) = \text{Hom}(R_\theta(V_1, \delta_1), R_\theta(V_2, \delta_2))$.*

*(iii) The sustainability criterion — colimit existence, non-triviality, and $|K|^2 > 0$ — is $R_\theta$-invariant.*

*Proof.* (i) $R_\theta$ maps objects to objects (if $\delta$ is a linear endomorphism, so is $e^{i\theta}\delta$). For morphisms: $h : (V_1, \delta_1) \to (V_2, \delta_2)$ satisfies $h \circ \delta_1 = \delta_2 \circ h$. Under $R_\theta$: $h \circ (e^{i\theta}\delta_1) = e^{i\theta}(h \circ \delta_1) = e^{i\theta}(\delta_2 \circ h) = (e^{i\theta}\delta_2) \circ h$, using linearity of $h$ and the fact that $e^{i\theta}$ is a scalar. So $h$ is also a morphism $(V_1, e^{i\theta}\delta_1) \to (V_2, e^{i\theta}\delta_2)$. $R_{-\theta}$ is the inverse.

(ii) By the calculation in (i), a linear map $h$ satisfies the intertwining condition for $(\delta_1, \delta_2)$ if and only if it satisfies it for $(e^{i\theta}\delta_1, e^{i\theta}\delta_2)$. The hom-sets are identical — the same linear maps, with the same vector space structure.

(iii) Since $R_\theta$ is a category automorphism, it preserves colimits: a diagram $D$ has a colimit if and only if $R_\theta(D)$ does, and the colimits are isomorphic. Since the hom-sets are identical (ii), the enriched hom-space sum $K(S,D) = \sum_{\text{chains}} \prod_{\text{morphisms}} (\text{coefficient})$ is unchanged. Therefore $|K(S,D)|^2$ is unchanged. $\square$

*Physical interpretation.* $R_\theta$ corresponds to rotating all phase references by $\theta$ — changing which direction in $\mathbb{C}$ each node calls "real." The theorem proves that this transformation changes descriptions (structure maps) but not relationships (morphisms) or outcomes (sustainability). This is the formal content of perspectivalism at quantum grain: no node's phase reference is privileged because the choice of reference has no effect on any observable.

*Note.* The proof establishes invariance under the full group $\mathbb{C}^* = \text{GL}(1, \mathbb{C})$, not just U(1): replacing $e^{i\theta}$ with any $z \in \mathbb{C}^*$ yields the same result. The restriction to U(1) $\subset$ $\mathbb{C}^*$ is physical, not mathematical: signal magnitude $|\sigma|$ is reference-independent (the same in all frames), while signal phase $\arg(\sigma)$ is reference-dependent (changes with the measuring node's convention). Perspectivalism demands invariance under conventional choices (phase rotation) but not under changes to physical quantities (magnitude scaling). The subgroup of $\mathbb{C}^*$ that changes phase without changing magnitude is U(1).

**Corollary** (Local invariance requires gauge connection). *Independent per-node phase rotations $\delta_i \mapsto e^{i\theta_i}\delta_i$ do not preserve morphisms: the intertwining condition $h \circ (e^{i\theta_s}\delta_s) = (e^{i\theta_t}\delta_t) \circ h$ requires $\theta_s = \theta_t$ for all connected pairs. Maintaining diagram coherence under local phase transformations requires compensating phase factors on morphisms — the categorical analogue of a gauge connection (see Section 6.5).*

**Corollary.** $\Sigma$ at quantum grain must support a U(1) action. The minimal such space is $\mathbb{C}$: real numbers support only the trivial $\{+1, -1\}$ action, which has no continuous rotation. Therefore $\Sigma = \mathbb{C}$ at quantum (electromagnetic) grain.

### 3.2 Enrichment and the Path Integral

At quantum grain, the relevant structure is the *dynamics-only functor* $G_\Sigma(V) = (\Sigma \to V)$, which captures the transition function without the output map. Working in $\textbf{Vect}_\mathbb{C}$ with finite-dimensional spaces, a $G_\Sigma$-coalgebra has structure map $V \to [\Sigma, V]$, which by currying is $V \otimes \Sigma \to V$. For $\Sigma = \mathbb{C}$, $[\mathbb{C}, V] \cong V$, so a $G_\mathbb{C}$-coalgebra reduces to $(V, \delta : V \to V)$ — a finite-dimensional vector space equipped with a linear endomorphism. $\text{Coalg}(G_\mathbb{C})$ over $\textbf{Vect}_\mathbb{C}$ is the category of such pairs — equivalently, the category of $\mathbb{C}[x]$-modules (where $x$ acts by $\delta$). It is cocomplete: module categories over any ring are cocomplete, with colimits constructed in the underlying abelian category.

This specialization is natural: the general framework uses $F_\Sigma$ (with outputs) at all grains, but the quantum alignment depends on the dynamics (convergence), not the output (transmission). The change from $F_\Sigma$ over $\textbf{Set}$ to $G_\Sigma$ over $\textbf{Vect}_\mathbb{C}$ involves two structural modifications — dropping the output map and changing the base category — motivated by the empirical observation that quantum systems exhibit interference (see pressure point 9). The framework accommodates this observation by providing a categorical setting in which interference is natural; it does not derive interference from first principles.

With $\Sigma = \mathbb{C}$, working in **Vect**$_\mathbb{C}$ (the category of complex vector spaces with linear maps):

**Theorem 2** (Enrichment). *$\text{Coalg}(G_\Sigma)$ over $\textbf{Vect}_\mathbb{C}$ is $\mathbb{C}$-enriched: the set of coalgebra morphisms between any two objects is a $\mathbb{C}$-vector subspace of the space of all linear maps, and composition is bilinear.*

*Proof.* A coalgebra morphism $h : (V_1, \delta_1) \to (V_2, \delta_2)$ satisfies $h \circ \delta_1 = \delta_2 \circ h$ (intertwining condition). If $h_1, h_2$ both satisfy this condition, then for any $\lambda, \mu \in \mathbb{C}$: $(\lambda h_1 + \mu h_2) \circ \delta_1 = \lambda(\delta_2 \circ h_1) + \mu(\delta_2 \circ h_2) = \delta_2 \circ (\lambda h_1 + \mu h_2)$. The zero map satisfies $0 \circ \delta_1 = 0 = \delta_2 \circ 0$. Therefore the hom-set is a linear subspace. Bilinearity of composition follows from linearity of the constituent maps. $\square$

Note: enrichment *fails* for the full Moore machine functor $F_\Sigma(V) = \Sigma \times (\Sigma \to V)$, because the output-preservation condition $\text{out}_2 \circ h = \text{out}_1$ yields $\text{out}_2 \circ (\lambda h_1 + \mu h_2) = (\lambda + \mu) \cdot \text{out}_1 \neq \text{out}_1$ in general. Precisely: the morphism set for the full functor is an *affine* subspace (shifted away from the origin by the output constraint), not a vector subspace. Interference requires a vector space (superposition of amplitudes); the output map locks hom-sets into affine spaces where linear combinations fail. The dynamics-only functor removes this constraint, yielding the vector space structure needed for quantum interference.

Linearity of transitions is not an independent assumption. Interference requires summing morphism chains in hom-spaces; summing requires hom-spaces to be vector spaces (enrichment); enrichment requires **Vect**$_\mathbb{C}$ as the base category; in **Vect**$_\mathbb{C}$, maps are linear by definition. Linearity is forced by the same empirical observation that motivates $\Sigma = \mathbb{C}$: quantum systems exhibit interference.

**Theorem 3** (Distributive Amplitude Sum). *In $\mathbb{C}$-enriched $\text{Coalg}(G_\Sigma)$, a diagram with multiple morphism chains from source $S$ to target $D$ produces a total amplitude in $\text{Hom}(S, D)$:*

$$K(S, D) = \sum_{\text{chains}} \prod_{\text{morphisms along chain}} (\text{coefficient})$$

*This is a distributive amplitude sum: each chain is a path, each morphism coefficient is a phase weight, and the sum is over all paths. The mechanism is bilinear distributivity of enriched composition: if $f_1 + f_2 \in \text{Hom}(A, B)$ and $g_1 + g_2 \in \text{Hom}(B, C)$, then $(g_1 + g_2) \circ (f_1 + f_2) = g_1 f_1 + g_1 f_2 + g_2 f_1 + g_2 f_2$. The sum over paths and the product of weights are consequences of distributivity in a $\textbf{Vect}_\mathbb{C}$-enriched category. For finite-dimensional systems, this is exact — not an approximation.*

**Example** (Double slit). Four $G_\mathbb{C}$-coalgebras $S, A, B, D$ with $\delta = \text{id}$. Morphisms $f_1 : S \to A$, $f_2 : S \to B$, $g_1 : A \to D$, $g_2 : B \to D$ with coefficients $e^{i\alpha_k}$, $e^{i\beta_k}$. Two composite chains: $g_1 \circ f_1 = e^{i\phi_1}$, $g_2 \circ f_2 = e^{i\phi_2}$. By enrichment, $\text{Hom}(S, D)$ is a $\mathbb{C}$-vector space containing both; their sum $K = e^{i\phi_1} + e^{i\phi_2}$ is well-defined. Sustainability: $|K|^2 = |e^{i\phi_1} + e^{i\phi_2}|^2$ — the double-slit interference pattern.

The correspondence between enriched hom-space computation and the Feynman path integral:

| Feynman Path Integral | Enriched Hom-Space Sum |
|---|---|
| Path $x(t)$ from $a$ to $b$ | Morphism chain in diagram |
| Phase weight $e^{iS/\hbar}$ | Product of morphism coefficients |
| $\sum_{\text{paths}}$ or $\int \mathcal{D}x$ | Sum in enriched hom-space |
| Propagator $K(b,a)$ | Total amplitude in $\text{Hom}(S, D)$ |
| $|K|^2$ = probability | Sustainability measure |

Two distinct operations contribute to the quantum alignment: *enrichment* gives interference (the amplitude sum), while *colimits* give constitution (the formation of new entities from diagrams). The Born rule bridges them: $|A|^2 > 0$ means the colimit forms (constitution succeeds); $|A|^2 = 0$ means destructive interference prevents constitution. The extension from discrete to continuous path integrals (the standard Feynman measure) remains an open step, relevant to quantum field theory but not required for finite-dimensional quantum mechanics.

### 3.3 Born Rule from Gleason's Theorem

The path integral formulation and the Hilbert space formulation of quantum mechanics are mathematically equivalent (Feynman, 1948). Gleason's theorem (1957): in a Hilbert space of dimension $\geq 3$, the unique consistent probability measure is $|\psi|^2$.

The derivation chain, with verification status:

$$\underset{\text{(empirical)}}{\text{phase signals}} \to \underset{\text{(proved, Thm 4)}}{\text{global U(1)}} \to \underset{\text{(minimal choice)}}{\Sigma = \mathbb{C}} \to \underset{\text{(empirical: interference)}}{\textbf{Vect}_\mathbb{C}} \to \underset{\text{(proved, Thm 2)}}{\text{enrichment}} \to \underset{\text{(proved, Thm 3)}}{\text{amplitude sum}} \to \underset{\text{(open, PP 10)}}{\text{Feynman PI}} \to \underset{\text{(requires inner product, PP 13)}}{\text{Hilbert space}} \to \underset{\text{(established, Gleason)}}{\text{Born rule}}$$

The chain has three formally proved steps (Theorems 2-4), three open structural gaps (PP 10: amplitude sum to Feynman path integral; PP 12: tensor product for multiparticle composition; PP 13: inner product for Hilbert space), and two invocations of established mathematics (Feynman equivalence, Gleason's theorem) contingent on closing the gaps.

Step 1 is the empirical premise (quantum signals have phase structure that produces interference). Step 2 is proved in this paper (Theorem 4: perspectivalism forces global phase invariance). Step 3 is the minimal choice: $\mathbb{C}$ is the simplest space supporting continuous U(1). Step 4 is an additional empirical premise: the observation of interference motivates the change to $\textbf{Vect}_\mathbb{C}$ (see pressure point 9). Steps 5-6 are proved in this paper (Theorems 2-3). Step 7 is a structural correspondence: the discrete hom-space sum has the form of a path integral, but the identification with Feynman's construction requires showing that the morphism coefficients satisfy the composition and unitarity axioms — argued here by structural match, not formally verified. Steps 8-9 are established mathematics applied if the correspondence holds. For finite-dimensional quantum systems, the derivation chain contains three formally proved steps, one structural correspondence (discrete hom-space sum to Feynman path integral — argued by structural match but not formally verified as satisfying the composition and unitarity axioms), and two invocations of established mathematics.

**Connection to the sustainability criterion.** The Born rule and the sustainability criterion play structurally analogous roles at different grains. At quantum grain, $|A|^2$ serves as the sustainability measure: phase destruction (lossy integration) produces magnitude. $|A|^2 > 0$: valid colimit, new node forms. $|A|^2 = 0$: no valid colimit, no node. At higher grains, the sustainability criterion operates on non-complex $\Sigma$ and produces topological coherence rather than phase coherence. The Born rule is the quantum-grain instance of the sustainability criterion, though the precise relationship between the binary general criterion and the continuous quantum measure ($|A|^2 \in [0, \infty)$) remains to be formalized.

### 3.4 Generalization to Gauge Groups

The perspectivalism argument is not specific to U(1). At each grain, "no privileged reference" produces the gauge group determined by the structure of $\Sigma$:

- Electromagnetic $\Sigma$ (phase on a circle): U(1)
- Weak force $\Sigma$ (2-component complex vectors): SU(2)
- Strong force $\Sigma$ (3-component color vectors): SU(3)
- Gravitational $\Sigma$: diffeomorphism invariance

One principle — perspectivalism — applied at each grain's empirically observed signal space, producing a gauge symmetry. This is not a prediction of which $\Sigma$ appears at which grain; $\Sigma$ is taken from known physics (see Section 6.4, pressure point 7). The claim is structural: given any $\Sigma$, perspectivalism produces invariance under transformations that preserve the signal structure.

A gap remains: perspectivalism produces invariance under the full automorphism group of $\Sigma$, which for $\mathbb{C}^n$ is $\text{GL}(n, \mathbb{C})$, not $\text{SU}(n)$. The restriction to unitary transformations (preserving inner product) and unit determinant requires additional structure — physically, conservation of probability and absence of a preferred phase convention. The framework does not yet derive these restrictions from its own principles; they are imported from the physics at each grain. This is an honest gap: the direction (perspectivalism $\to$ gauge symmetry) is correct, but the specific gauge group requires constraints beyond perspectivalism alone. Discrete symmetries (parity, charge conjugation, time reversal) are also not addressed; the weak force's parity violation remains outside scope.

### 3.5 Classical Limit as Grain Transition

The quantum/classical boundary dissolves. At quantum grain, $\Sigma = \mathbb{C}$ (complex phase space): $\mathbb{C}$-enrichment produces interference, superposition, and entanglement. At higher grains (molecular, cellular), $\Sigma$ = chemical, electrical — signals no longer carry raw quantum phase. The enrichment structure dilutes.

Decoherence is grain transition: the point where $\Sigma$ changes from complex to non-complex, and the path integral structure gives way to classical dynamics.

---

## 4. Framework Reading of Standard Results

The following subsections demonstrate compatibility between the framework and known quantum phenomena. These are consistency checks — the framework's language applied to established results — not independent derivations. Where the framework adds interpretive value beyond restating known physics, this is noted explicitly.

### 4.1 Superposition

A system that has not been integrated by a given node has no definite state relative to that node (Section 2.5). This IS superposition. The system is not "in multiple states simultaneously" — there is no fact of the matter until a colimit forms. This reading is ontological, not epistemic: it is demanded by the framework's own commitments (state = integration; no integration = no state). It is structurally identical to Rovelli's relational QM interpretation.

### 4.2 Double-Slit Experiment

Two paths with phases $\phi_1, \phi_2$. Amplitude at detector (enriched hom-space sum): $A(D) = e^{i\phi_1} + e^{i\phi_2}$. Sustainability: $|A|^2 = |e^{i\phi_1} + e^{i\phi_2}|^2$. Constructive interference (bright fringe) when paths differ by integer wavelengths; destructive (dark fringe) when they differ by half-wavelength. Matches QM prediction and experiment.

### 4.3 Three-Slit / Sorkin Test

Three paths: $A(D) = e^{i\phi_1} + e^{i\phi_2} + e^{i\phi_3}$ (enriched hom-space sum). The sustainability measure $|A|^2$ decomposes into individual and pairwise terms. No three-way or higher-order interference terms appear. This is because the Born rule is quadratic — a consequence of the linear path sum and the $|\cdot|^2$ sustainability measure. Confirmed experimentally to high precision.

### 4.4 Which-Path Information

Detector at one slit constitutes a new node (colimit formation). Signal consumed. New signal emitted. Only one path to the detector remains. No sum. No interference. Matches QM and experiment.

### 4.5 Entanglement and Bell Correlations

Entangled pair = one colimit at quantum grain (single constituted entity). Measurement fragments the colimit. Fragments inherit colimit structure (correlations from shared constitution, not transmitted between particles). Note: "colimit fragmentation" and "structure inheritance" are physical narratives describing the intended categorical mechanism; the formal construction of how a colimit decomposes under measurement and how the resulting pieces retain correlation structure is not yet developed.

For an entangled photon pair: $E(\alpha, \beta) = -\cos 2(\alpha - \beta)$. CHSH value: $2\sqrt{2}$ (Tsirelson bound). These results depend on Hilbert space structure with tensor product composition and inner product — structural features the framework has not yet produced (pressure points 12, 13). If the open gaps in the derivation chain can be closed, the Tsirelson bound would follow from established mathematics (Cirel'son, 1980). The results are stated here as consistency targets, not as framework consequences.

### 4.6 Bell Test Survival

The framework does not reduce to a local hidden variable (LHV) theory. This is not merely consistent with the framework — it is *demanded* by it. The ontological reading (no fact exists until integration) follows necessarily from the framework's own commitments: state = integration (colimit); no integration = no state. There is nothing hidden because there is genuinely nothing until the colimit forms. This is structurally distinct from an LHV theory, which posits definite but unknown values prior to measurement. In this framework, there are no values — definite or otherwise — prior to constitution.

### 4.7 Wigner's Friend

The Wigner's Friend paradox requires a privileged observer (Wigner) whose perspective determines when collapse "really" occurs. The framework has no privileged observers. Constitution events are perspectival (Section 2.5): the friend's measurement constitutes a new node relative to the friend's diagram; Wigner's measurement constitutes a new node relative to Wigner's diagram. Cross-perspective consistency is guaranteed by topology: when Wigner integrates with the friend, they integrate with a dense network of already-constituted, mutually-consistent nodes. The paradox dissolves because its premise (one observer's perspective is privileged) is denied by the framework.

### 4.8 Measurement Problem

The measurement problem asks: why does measurement produce a definite outcome? In the framework, the structural question is resolved: valid colimits form when integration succeeds per the sustainability criterion. The mechanism of collapse is constitution. The remaining open question is statistical: why *this* outcome at *this* probability? This is the Born rule question, addressed by the derivation chain in Section 3.

---

## 5. Predictions and Falsification

### 5.1 Quantitative Predictions

Three predictions unified as measurements of one geometric structure:

1. **Energy-compression log scaling.** The Landauer cost of staged compression at each grain follows a logarithmic scaling relation.

2. **Power-law betweenness with $\Sigma$-determined exponent.** Sustainable systems exhibit power-law betweenness distributions. The exponent is determined by $\Sigma$ at the relevant grain. The same network under different $\Sigma$-constraint regimes shows different exponents. This distinguishes the framework from preferential attachment models (Barabasi): same observable, different generative mechanism, different exponent predictions.

3. **Keystone cascade follows morphism structure.** Removal of high-betweenness nodes produces cascades following the colimit's dependency structure.

### 5.2 Failure Mode Predictions

The three failure modes (fragmentation, condensation, rate-exceeds-modulation) produce measurably distinct topological signatures in network betweenness distributions. These signatures should be domain-invariant:

- **Ecosystem collapse:** fragmentation signature (flat betweenness) or rate-exceeds-modulation
- **Financial crisis:** condensation signature (extreme betweenness concentration in hub nodes)
- **Neural dysfunction:** failure mode dependent on pathology
- **Cancer:** condensation (oncogene-driven pathway dominance — constitutive activation routes all signaling through a few hyperactivated nodes, reducing distributed coordination). This signature is expected in the *transition* from healthy to cancer; a static snapshot of a cancer network captures the endpoint, not the directional change. A direct test would compare healthy and cancer tissue signaling topologies.

The strongest test: the same three structural signatures appearing across independent domains in data collected for purposes unrelated to this framework. A concrete test design: take four domains (ecological food webs, bank lending networks, connectome data, gene regulatory networks), measure betweenness distributions before and during system failure, and compare against the predicted failure mode signature for each domain. If the predicted signatures appear in all four, using data collected by domain scientists for unrelated purposes, the result is difficult to dismiss as artifact.

### 5.3 Cross-Domain Empirical Observation

To test whether the failure mode taxonomy applies across domains, we applied the same analysis protocol to three networks from independent fields: ecology, cancer biology, and neuroscience. All three datasets were collected for purposes unrelated to this framework. Analysis code and a generic failure mode analysis tool are available at [github.com/helyn-research/constitution-as-colimit](https://github.com/helyn-research/constitution-as-colimit).

A methodological note: these empirical networks are adjacency data (connectivity graphs), not full coalgebraic diagrams — they lack specified state spaces $S$ and structure maps $\delta$ for each node. The analysis tests the *topological* predictions of the failure mode taxonomy (betweenness distribution signatures under perturbation), not the full coalgebraic model. This is the topological shadow of the theory, not a direct test of the coalgebraic construction. Specifically, the mapping from "cocone factoring through a bottleneck" to "high betweenness Gini" and from "disconnected diagram" to "betweenness Gini flattening" is a heuristic motivated by structural analogy, not derived from the colimit construction (see pressure point 11). The empirical section tests the failure mode *taxonomy* as a classification scheme, not the coalgebraic apparatus that motivates it.

**Datasets.**

| Domain | Network | Nodes | Edges | Type | Source |
|---|---|---|---|---|---|
| Ecology | Little Rock Lake food web (Martinez, 1991) | 183 | 2,494 | Directed (prey $\to$ predator) | KONECT |
| Cancer biology | Cancer driver gene interactions (COSMIC Tier 1) | 411 | 574 | Undirected (protein associations) | STRING v12 |
| Neuroscience | *C. elegans* connectome (White et al., 1986) | 297 | 2,148 | Undirected (synaptic connections) | KONECT |

The food web uses trophic species (taxa aggregated by identical predator/prey sets); node connectivity reflects aggregated trophic roles. The cancer network is a curated subset: 30 Tier 1 cancer driver genes from the COSMIC Cancer Gene Census and their high-confidence interaction partners (STRING confidence $\geq$ 900); it is not a complete network of any biological system, and its hub-and-spoke structure reflects the query design. The connectome is a complete mapping of all 297 neurons and their synaptic connections in *C. elegans*.

**Method.** For each network, we computed betweenness centrality distributions and simulated two perturbation regimes: (1) *targeted hub removal* — sequentially removing the highest-betweenness node, recomputing after each removal (30 steps); (2) *random removal* — removing nodes in random order (30 steps, averaged over 20 trials). We tracked the Gini coefficient of the betweenness distribution (0 = uniform, 1 = maximally concentrated), computed both over the full network and within the largest connected component only (to control for finite-size artifacts). For the cancer network, we additionally tested (3) *cancer driver removal* — removing the 30 known driver genes in order of their betweenness. The targeted-vs.-random comparison follows the robustness protocol of Albert et al. (2000).

**Results.**

| Domain | Baseline Gini | Hub removal $\Delta$Gini | Random $\Delta$Gini | Signature |
|---|---|---|---|---|
| Ecology | 0.84 | $-$0.10 | $+$0.004 | **Fragmentation** |
| Cancer | 0.92 | $+$0.02 | $+$0.000 | **Condensation** |
| Neuroscience | 0.74 | $-$0.08 | $+$0.001 | **Fragmentation** |

**Null model comparison.** To test whether the signatures above reflect genuine network structure or degree-sequence artifacts, we generated configuration model null graphs per network: 500 nulls for baseline Gini comparison, 100 nulls for trajectory comparison (10-step targeted removal). Each null preserves the exact degree sequence of the real network but randomizes wiring. Betweenness centrality for real networks was computed exactly; for null models, approximate betweenness was used ($k = 150$ pivot nodes per computation) for computational tractability. For the food web ($N = 183$), $k = 150$ samples most of the network; for the cancer network ($N = 411$), $k = 150$ samples approximately 36% of nodes, introducing non-trivial variance in individual null estimates, though this is mitigated by averaging over 100 nulls.

| Domain | Real baseline | Null mean baseline | p(baseline) | Real $\Delta$Gini | Null mean $\Delta$Gini | Null sig types | p(trajectory) |
|---|---|---|---|---|---|---|---|
| Ecology | 0.84 | 0.63 | $<$0.01 | $-$0.10 | $+$0.04 | 84% condensation, 16% neutral | $<$0.01 |
| Cancer | 0.92 | 0.91 | $<$0.01 | $+$0.02 | $+$0.02 | 72% condensation, 28% neutral | 0.58 |
| Neuroscience | 0.74 | 0.67 | $<$0.01 | $-$0.08 | $-$0.11 | 100% fragmentation | $<$0.01* |

*For C. elegans, p $<$ 0.01 indicates the real network is *more robust* than all null models — it shows less fragmentation under hub removal than any configuration model null with the same degree sequence.

All three networks have structurally elevated baseline Gini (p $<$ 0.01 in all cases). The trajectories diverge. The food web fragmentation trajectory (p $<$ 0.01) is the strongest result: null models with the same degree sequence produce condensation — the *opposite* signature — while the real food web produces fragmentation. The food web's topology resists what its own degree sequence would predict. The cancer condensation trajectory (p = 0.58) is not distinguishable from a random same-degree network; 72% of nulls produce equal or greater condensation. The C. elegans connectome shows fragmentation in both real and all nulls, but the real network is more robust than any null, suggesting biological optimization for hub-removal resilience beyond what degree sequence alone confers.

In all three domains, random removal leaves the betweenness distribution unchanged ($\Delta$Gini $<$ 0.005). This is the well-known robustness of complex networks to random failure (Albert et al., 2000).

Under targeted hub removal, two distinct signatures emerge:

- *Fragmentation* (ecology, neuroscience): Gini drops — the network loses its hub structure, betweenness distributes more evenly. The food web Gini drops from 0.84 to 0.74; the connectome from 0.74 to 0.66. Both signatures persist when Gini is computed within the largest connected component only, confirming they are not finite-size artifacts.

- *Cancer* (cancer): Gini rises slightly under targeted hub removal (+0.02). **Null model result:** this trajectory is not unusual — 58% of 100 configuration model nulls produced equal or greater condensation (p = 0.58). The cancer network's condensation trajectory is a degree-sequence artifact: it is what any sparse, hub-heavy network with this degree distribution does when hubs are removed. The elevated baseline Gini (0.92 vs. null mean 0.91) is structural (p $<$ 0.01), but this is a static property — the network is more hub-dominated than degree sequence alone predicts — not a distinctive dynamic signature.

In the cancer network, 28 of 30 known cancer driver genes rank in the top 30 by betweenness centrality (TP53 is #1, CTNNB1 #2, MYC #3). This ranking is largely a construction artifact: the network was built by querying these 30 genes and their interaction partners, so seed genes will dominate betweenness in the resulting hub-and-spoke topology by design. Removing cancer drivers specifically produces a marginally stronger condensation signal ($\Delta$Gini $= +0.03$) than generic hub removal ($\Delta$Gini $= +0.02$); this difference of 0.01 is not statistically tested and should not be over-interpreted.

**Interpretation.** The differential response to targeted vs. random removal is well-established in network science (Albert et al., 2000; Dunne et al., 2002) and does not by itself test any prediction specific to this framework. What the cross-domain comparison adds is the observation that *different networks show different failure mode signatures under the same protocol*. The framework provides a structural interpretation: fragmentation corresponds to the first failure mode (disconnected diagram, no connected colimit); condensation corresponds to the second (cocone factoring through a single bottleneck node).

However, the three networks differ in density (0.007 to 0.075), directedness (two undirected, one directed), and construction method (two complete surveys, one curated query). Configuration model null model comparison (reported above) was performed to disentangle these effects. The ecology fragmentation signature is structural — null models produce condensation, the opposite signature. The cancer condensation trajectory is not structural — it is generic to any sparse network with this degree distribution. The C. elegans fragmentation type is shared with null models, but the real network is more robust than any null, suggesting additional structural organization beyond degree sequence.

**Limitations.** The fragmentation/condensation classification uses a Gini delta threshold of 0.02, chosen as the minimum magnitude that distinguishes a directional trend from noise. The cancer network's delta (+0.02) sits exactly on this boundary; at a threshold of 0.025, it would be classified as "neutral." The classification should be interpreted alongside continuous delta values and null model p-values, not as a sharp binary. The configuration model null preserves degree sequence but destroys higher-order structure such as trophic levels in food webs. The food web fragmentation result may reflect trophic organization (which the configuration model eliminates) rather than a novel structural property; a niche model null (Williams & Martinez, 2000) that preserves trophic structure would be needed to distinguish these explanations. All three analyses use simulated instantaneous node removal, not observed natural system failure with dynamics. The targeted-vs.-random comparison is a standard robustness protocol, not a novel test design. The cancer network is a curated query-based subset, not a complete biological network — its condensation signature may partly reflect the hub-and-spoke structure inherent in the query design. The targeted removal protocol removes nodes by betweenness centrality and then measures change in the betweenness distribution (Gini), introducing circularity; degree-targeted removal would be needed to confirm that the signature type is independent of the removal criterion. The analyses do not include secondary extinction cascading. Section 5.1 predicts power-law betweenness with $\Sigma$-determined exponents, but no power-law fitting is performed in Section 5.3 — the Gini analysis tests the qualitative failure mode taxonomy, not the quantitative exponent prediction. All networks have $N < 500$; scalability to larger networks has not been tested. Null model comparison (degree-preserving configuration model) has been performed; results are reported above. All networks are unweighted. Three datasets from three domains constitute a preliminary observation, not a systematic validation. Additional food webs, gene regulatory networks, and connectomes would be needed to establish generality within each domain before claiming generality across domains. The analyses show that the same tool produces classifiably different signatures across domains, consistent with the framework's taxonomy — but do not rule out that these differences are driven by network topology (density, degree distribution) rather than domain-specific biological structure.

### 5.4 Structural Prediction

Gleason's theorem requires Hilbert space dimension $\geq 3$ for the Born rule to be the unique consistent probability measure. In dimension 2, other measures are consistent. This is a structural prediction: the Born rule's uniqueness requires sufficient complexity ($\geq 3$ independent options) at the constitution event.

### 5.5 Falsification Criteria

**Empirical tests specific to the framework** (would falsify the framework while leaving standard physics intact):

1. **Failure mode signatures absent.** The predicted topological signatures (fragmentation, condensation, rate-exceeds-modulation) do not appear in cross-domain system failure data, or appear but are not domain-invariant — different domains show different failure taxonomies with no shared structure. (The cross-domain null model comparison in Section 5.3 finds structural fragmentation in ecology (p $<$ 0.01; null models produce the opposite signature) and structural baseline elevation in neuroscience (p $<$ 0.01; connectome more robust than any null). The cancer condensation trajectory does not survive null model comparison (p = 0.58). The third failure mode, rate-exceeds-modulation, has not been tested. The observation is preliminary; see Section 5.3 limitations.)
2. **Betweenness exponents are $\Sigma$-independent.** The same network under different $\Sigma$-constraint regimes shows the same exponent, contradicting the prediction that the exponent is $\Sigma$-determined.
3. **Stable persistence through uncompensated instability.** A higher-level system that persists through persistent, uncompensated lower-level instability on timescales long relative to the instability — no response or cascade observed.

**Mathematical validity checks** (would invalidate the formal apparatus, not empirically falsify the framework):

4. A formal error in the colimit construction (Section 2).
5. A demonstration that the $\mathbb{C}$-enriched hom-space sum does not produce path integral structure (Section 3.2).

**Shared with standard QM** (would falsify the framework and QM simultaneously):

6. Higher-order interference terms in multi-slit experiments.

---

## 6. Discussion

### 6.1 What This Is Not

This is not a relabeling of quantum mechanics. The Tsirelson bound explanation (inner product constraint from Hilbert space structure), the classical limit as grain transition (change in $\Sigma$), and the Born rule derivation from perspectivalism are explanatory additions, not renaming.

This is not a complete proof. The Born rule derivation chain has three formally proved steps (global U(1) invariance, enrichment, and distributive amplitude sum), one structural correspondence (discrete sum to Feynman path integral — argued by structural match, not formally verified), and two steps invoking established mathematics (Feynman equivalence, Gleason's theorem). The restriction from $\mathbb{C}^*$ to U(1) rests on a physical interpretation (magnitude is reference-independent, phase is not), not a derivation. The extension to continuous path integrals (quantum field theory) is open.

This is not a claim to replace quantum mechanics. QM's mathematical apparatus is correct. The framework provides a context within which QM's postulates become theorems — if the argument holds.

### 6.2 Folk-Category Dissolutions

The framework systematically dissolves hard categorical boundaries into continua. Examples include: hierarchy (reframed as connection density at different observation grains), boundary (reframed as $\Sigma$-determined interface), locality (reframed as signal-type compatibility defining neighborhood), and observer/observation/observed (reframed as three descriptions of one event). Historical precedent supports this pattern (vitalism $\to$ biochemistry, phlogiston $\to$ oxidation, aether $\to$ relativity). The concern that the framework finds what it is designed to find is acknowledged; the test is whether it can recognize a genuine boundary. The full list of dissolutions and their broader implications are available in the supplementary theory document.

### 6.3 Prior Challenge History

The framework has undergone structured adversarial challenge during its development, using Claude instances prompted to role-play domain experts (philosophy of science, category theory, quantum foundations, network science, biology/ecology, and a critical skeptic) and independent external review (Gemini 3.1 Pro, domain-specific reviews in category theory, quantum foundations, network science, and philosophy of science). This is not independent peer review — it is structured challenge using AI, and should be evaluated as such. The method's value lies in systematic pressure-testing from multiple disciplinary perspectives simultaneously; its limitations are that AI reviewers share training distributions, and the framework was co-developed with one of the reviewing systems (Claude). No independent human domain experts have reviewed this work. The pressure points listed below are the concerns that have survived this process; they represent convergent findings across multiple AI reviewers and should be treated as identified risks, not resolved issues.

### 6.4 Known Pressure Points

Stated in the interest of intellectual honesty and to focus scrutiny where it is most productive:

1. **Derivation chain partially verified.** Global U(1) invariance (Theorem 4), enrichment (Theorem 2), and the distributive amplitude sum (Theorem 3) are proved. The restriction from $\mathbb{C}^*$ to U(1) rests on physical interpretation (magnitude vs. phase reference-dependence). The step from distributive amplitude sum to Feynman path integral is a structural correspondence, not a formal equivalence (see pressure point 10). The continuous limit (quantum field theory) is open. The Feynman and Gleason steps invoke established mathematics.

2. **Limited empirical testing.** A cross-domain null model comparison (Section 5.3) finds that the food web fragmentation signature is structural (p $<$ 0.01; null models with the same degree sequence produce condensation — the opposite signature). The C. elegans connectome shows structural baseline elevation and greater robustness than any same-degree null. The cancer condensation trajectory is a degree-sequence artifact (p = 0.58); only the elevated baseline Gini is structural. The cross-domain comparison of signature *type* survives for ecology; it is ambiguous for neuroscience (same type as nulls, but more robust); it does not survive for cancer. The $\Sigma$-determined exponents remain untested — no specific exponent has been derived from the colimit construction.

3. **Tautology risk.** "What coheres, persists" is near-tautological. The non-tautological content is the structural claim: coherence at each grain is independently assessable.

4. **Parity violation outside scope.** The perspectivalism argument produces continuous gauge symmetries but does not address discrete symmetries.

5. **Quantum field theory gap.** Pair production is handled as bidirectional constitution. The full QFT operator formalism has not been mapped.

6. **Coherence may be rare.** We may be an island of deep coherence, not evidence of universal tendency. Implications for predictions not yet assessed.

7. **$\Sigma$ is externally supplied.** The framework does not predict the signal space at any grain; it takes $\Sigma$ as empirical input. The quantum alignment depends on the observation that quantum-grain signals are phase patterns. The framework explains what follows from $\Sigma$, not why $\Sigma$ takes the form it does.

8. **Gauge group restriction.** Perspectivalism produces invariance under the full automorphism group of $\Sigma$, which is $\text{GL}(n, \mathbb{C})$ for $\mathbb{C}^n$ — not the physically correct $\text{SU}(n)$. The restriction to unitary, unit-determinant transformations requires additional structure (probability conservation, absence of preferred phase) not yet derived from the framework's own principles.

9. **Functor and base category switch.** The general emergence framework (Section 2) uses $F_\Sigma$ over $\textbf{Set}$. The quantum alignment (Section 3) uses the dynamics-only functor $G_\Sigma$ over $\textbf{Vect}_\mathbb{C}$. This involves two structural changes — dropping the output map and changing the base category — not just a parametric specialization of $\Sigma$. The change to $\textbf{Vect}_\mathbb{C}$ is motivated by the observation of interference (Section 3.2), but it is an additional premise, not a derivation. A deeper tension: ontological commitment 2 (mutual conditioning) requires nodes to emit and receive signals via the output map. Dropping the output map to achieve enrichment means quantum-grain nodes no longer emit signals in the formal sense — morphisms replace signal exchange as the interaction mechanism. This is not just a technical modification; it changes the ontological picture at quantum grain.

10. **Discrete-to-path-integral correspondence.** Theorem 3 produces a sum over morphism chains with complex coefficients — bilinear distributivity of composition in a $\mathbb{C}$-enriched category. This has the algebraic form of a distributive amplitude sum. The identification with the Feynman path integral requires showing that the morphism coefficients correspond to $e^{iS/\hbar}$ for an action functional, that the composition law for propagators is satisfied, and that the diagram represents a discretization of the path space. A deeper obstacle: coalgebraic morphisms satisfy an intertwining condition ($h \circ \delta_1 = \delta_2 \circ h$), which constrains morphisms to be *compatible with* the dynamics — producing selection rules and conservation laws. The Feynman propagator, by contrast, *implements* the dynamics. These are different mathematical relationships, and bridging them is the central open problem of the quantum alignment.

11. **Theory-to-metrics gap.** The empirical observation (Section 5.3) uses the Gini coefficient of betweenness centrality as a proxy for colimit structure. The mapping from "cocone factoring through a bottleneck" to "high betweenness concentration" and from "disconnected diagram" to "betweenness flattening under perturbation" is heuristic — motivated by structural analogy, not derived from the colimit construction. A formal derivation would require defining a measure of cocone concentration within the coalgebraic framework and proving that it correlates with betweenness concentration in the underlying graph. Without this derivation, the empirical observation tests the failure mode taxonomy as a classification scheme, not as a consequence of the colimit construction.

12. **Composition vs. constitution.** Colimits model constitution (parts integrating into a whole), producing direct sums (coproducts) in $\textbf{Vect}_\mathbb{C}$. But quantum mechanics composes independent systems via tensor products ($V \otimes W$), not direct sums ($V \oplus W$). Tensor products are what create entanglement — joint states that cannot be factored into individual states. The framework currently treats entanglement as "one colimit" (Section 4.5) but does not address how independent systems compose to form joint state spaces. A monoidal structure on $\text{Coalg}(G_\mathbb{C})$ — where the monoidal product corresponds to the tensor product — would be needed to handle multiparticle quantum mechanics.

13. **Missing inner product.** The derivation chain produces $\textbf{Vect}_\mathbb{C}$ (complex vector spaces) but not $\textbf{Hilb}$ (Hilbert spaces). The difference: Hilbert spaces carry an inner product, which defines $|\psi|^2$ in a basis-independent way. Without an inner product, the sustainability measure $|A|^2$ lacks a basis-independent definition. Gleason's theorem requires a Hilbert space, not merely a vector space. The inner product is also what restricts the symmetry group from $\text{GL}(n, \mathbb{C})$ to $\text{U}(n)$ (pressure point 8) — these are aspects of the same gap.

### 6.5 Open Questions

- Formalize sustainability criterion condition (c): define "rate of change" and "modulation capacity" within the coalgebraic framework
- Formalize gauge connection from local perspectivalism: Theorem 4 proves global phase invariance; the corollary shows local invariance requires compensating morphism phases (gauge connection). The natural categorical tool is the Grothendieck construction: local phase variation fibers $\text{Coalg}(G_\mathbb{C})$ over $U(1)$, and morphisms in the fibered category carry phase discrepancies whose composition yields holonomy. Formalizing this — including curvature and the relationship to the electromagnetic potential — is the natural next step
- Discrete-to-continuous limit: verify that the coalgebraic path sum recovers the standard Feynman measure
- Derive at least one specific numerical prediction (e.g., a betweenness exponent for a specific system) from $\Sigma$ and the colimit construction
- Prove exhaustiveness of three failure modes from the colimit construction
- Universality theorem: prove power-law topology is the universal signature of sustainable convergence for any $\Sigma$
- Derive Landauer cost from colimit lossiness without thermodynamic inheritance
- Arrow of time from a timeless pre-spacetime network
- Signal consumption: colimits operate on state spaces and structure maps, not on signals directly. The mechanism by which a signal is "consumed" during constitution is not modeled by the colimit construction. Alternative constructions (e.g., pushouts along signal-to-state embeddings) may be needed.
- Gauge group restriction: perspectivalism produces $\text{GL}(n, \mathbb{C})$ invariance, not $\text{SU}(n)$. Derive unitarity and unit determinant from framework principles, or identify the additional structure required.
- Spin and fermionic statistics: the framework operates at electromagnetic grain with $\Sigma = \mathbb{C}$ (scalar). Spin-1/2 systems require SU(2) representations and spinor structure, which the current $\Sigma = \mathbb{C}$ setup does not address. Fermionic statistics (anti-commutation, Pauli exclusion) are not modeled by the coalgebraic construction as presented
- Theory-to-metrics bridge: derive the relationship between cocone concentration and graph-theoretic measures (betweenness centrality, Gini coefficient) from the coalgebraic framework, closing the gap between the theoretical failure mode taxonomy and the empirical signatures used to test it
- Monoidal structure for composition: identify a monoidal product on $\text{Coalg}(G_\mathbb{C})$ that corresponds to the tensor product on $\textbf{Vect}_\mathbb{C}$, enabling the framework to handle composition of independent quantum systems and multiparticle entanglement
- Inner product from sustainability: determine whether the sustainability criterion or another structural feature of the coalgebraic framework can ground a canonical inner product on hom-spaces, bridging from $\textbf{Vect}_\mathbb{C}$ to $\textbf{Hilb}$ and providing basis-independent meaning to $|A|^2$
- Unitarity vs. lossiness: quantum evolution is unitary (information-preserving), but colimits of connected diagrams are lossy quotients. How do these coexist at the quantum grain? A possible resolution: lossiness appears only at grain transitions (decoherence), not within quantum-grain evolution. But this requires a formal account of when colimits are information-preserving (within a grain) vs. lossy (across grains)
- Diagram individuation: the colimit construction requires a specific diagram as input, but the framework provides no formal mechanism for selecting which subset of the universal interaction graph forms a diagram. What localizes constitution events?
- Strict morphisms at macro grains: coalgebraic morphisms require exact commutation with structure maps. In noisy, asynchronous biological systems, exact algebraic alignment between interacting entities is unrealistic. The framework may need lax morphisms, approximate colimits, or a shift to probabilistic base categories (e.g., categories of Markov kernels) to model emergence at biological and social grains faithfully
- Inter-grain Σ transition: a colimit in $\text{Coalg}(F_{\Sigma_1})$ produces a new object in the *same* category with the *same* $\Sigma_1$. But the paper claims $\Sigma$ changes by grain (electromagnetic → chemical → behavioral). The formal mechanism by which a colimit at one grain generates entities operating in a different signal space is entirely missing — this is the grain transition problem
- Full QFT mapping at quantum field grain

---

## 7. Conclusion

We presented a coalgebraic model of emergence in which constitution is modeled as the categorical colimit of Moore machine coalgebra diagrams. The framework produces a sustainability criterion with three failure modes (fragmentation, condensation, rate-exceeds-modulation), and a cross-domain null model comparison finds that the food web fragmentation signature is structural — degree-preserving random networks produce the opposite signature — while the cancer condensation trajectory is a degree-sequence artifact. The C. elegans connectome is more robust to hub removal than any same-degree random graph. The food web result is the strongest empirical finding: the real topology actively resists what its own degree sequence would predict.

When instantiated at quantum grain with two empirical premises (phase signals and interference) and one structural change (the dynamics-only functor over $\textbf{Vect}_\mathbb{C}$ rather than the full functor over $\textbf{Set}$), the framework produces structural parallels to quantum mechanics: $\mathbb{C}$-enrichment (Theorem 2), a distributive amplitude sum with the algebraic form of a path integral (Theorem 3), and global U(1) phase invariance (Theorem 4). The identification of the discrete sum with the Feynman path integral remains an open problem — argued by structural match but not formally verified. If this correspondence can be established, the Born rule would follow via established mathematics (Feynman's equivalence, Gleason's theorem). The quantum alignment is a research program that invites collaboration from physicists and category theorists; it is not a completed derivation.

The core construction — constitution as colimit of Moore machine coalgebras — rests on two ontological commitments (constitution and mutual conditioning), one principle (perspectivalism), two empirical premises ($\Sigma = \mathbb{C}$, interference), and one structural choice (base category). The predictions are stated, the falsification criteria are specific, the pressure points are identified, and the framework is open for challenge.

---

## References

Abramsky, S. & Coecke, B. (2004). A categorical semantics of quantum protocols. *Proceedings of the 19th Annual IEEE Symposium on Logic in Computer Science*, 415--425.

Adámek, J. & Rosický, J. (1994). *Locally Presentable and Accessible Categories*. Cambridge University Press.

Albert, R., Jeong, H., & Barabási, A.-L. (2000). Error and attack tolerance of complex networks. *Nature*, 406(6794), 378--382.

Ashby, W. R. (1956). *An Introduction to Cybernetics*. Chapman & Hall.

Barabási, A.-L. & Albert, R. (1999). Emergence of scaling in random networks. *Science*, 286(5439), 509--512.

Chiribella, G., D'Ariano, G. M., & Perinotti, P. (2011). Informational derivation of quantum theory. *Physical Review A*, 84(1), 012311.

Cirel'son, B. S. (1980). Quantum generalizations of Bell's inequality. *Letters in Mathematical Physics*, 4(2), 93--100.

Dunne, J. A., Williams, R. J., & Martinez, N. D. (2002). Network structure and biodiversity loss in food webs: robustness increases with connectance. *Ecology Letters*, 5(4), 558--567.

Feynman, R. P. (1948). Space-time approach to non-relativistic quantum mechanics. *Reviews of Modern Physics*, 20(2), 367--387.

Friston, K. (2010). The free-energy principle: a unified brain theory? *Nature Reviews Neuroscience*, 11(2), 127--138.

Gleason, A. M. (1957). Measures on the closed subspaces of a Hilbert space. *Journal of Mathematics and Mechanics*, 6(6), 885--893.

Hardy, L. (2001). Quantum theory from five reasonable axioms. arXiv:quant-ph/0101012.

Kelly, G. M. (1982). *Basic Concepts of Enriched Category Theory*. Cambridge University Press. Reprinted in *Reprints in Theory and Applications of Categories*, No. 10, 2005.

Martinez, N. D. (1991). Artifacts or attributes? Effects of resolution on the Little Rock Lake food web. *Ecological Monographs*, 61(4), 367--392.

Maturana, H. R. & Varela, F. J. (1980). *Autopoiesis and Cognition: The Realization of the Living*. D. Reidel.

Rovelli, C. (1996). Relational quantum mechanics. *International Journal of Theoretical Physics*, 35(8), 1637--1678.

Szklarczyk, D. et al. (2023). The STRING database in 2023: protein-protein association networks and functional enrichment analyses for any sequenced genome of interest. *Nucleic Acids Research*, 51(D1), D638--D646.

Tate, J. G. et al. (2019). COSMIC: the Catalogue Of Somatic Mutations In Cancer. *Nucleic Acids Research*, 47(D1), D941--D947.

van Inwagen, P. (1990). *Material Beings*. Cornell University Press.

Tononi, G. (2004). An information integration theory of consciousness. *BMC Neuroscience*, 5, 42.

von Bertalanffy, L. (1968). *General System Theory: Foundations, Development, Applications*. George Braziller.

White, J. G., Southgate, E., Thomson, J. N., & Brenner, S. (1986). The structure of the nervous system of the nematode *Caenorhabditis elegans*. *Philosophical Transactions of the Royal Society of London B*, 314(1165), 1--340.

Whitehead, A. N. (1929). *Process and Reality*. Macmillan.

Williams, R. J. & Martinez, N. D. (2000). Simple rules yield complex food webs. *Nature*, 404(6774), 180--183.
