# Novelty audit — construct-identified inference (2026-09-12)

Adversarial. The question was: can the framework be claimed as novel, pioneering, or at least minority-of-adopters?

## 1. Closest prior art

1. **Chen, Rambachan & Tamer (2026).** *Partial Identification from LLM Prompts.* arXiv:2606.15031 (v2 24 Jun 2026). [1]
   LLM reports as measures of a latent label; PI of prevalence θ under arbitrarily dependent errors; identifying power from externally calibrated scores; extension to regression when the latent is a regressor. **Gap:** restrictions are distributional / benchmark-informed, not nomological pass/fail tests over a finite menu. Object of inference is θ (or a coefficient), not an admissible measurement set M*.

2. **Ogut & Yin (2026).** *Partial Identification with Multiple Nonlinear Measurements of a Latent Regressor.* arXiv:2607.12219 (13 Jul 2026). [2]
   Same destination as cvprofiles: [L,U] for β over multiple measurements. Curvature-bound engine + factor-analytic drop of a discordant source. Application: six AI-exposure measures, ACS 8.88M person-years. **Gap:** interval from smoothness/curvature under a linear-consensus normalization, not from researcher-specified nomological restrictions. Measures are noisy functions of one latent, not rival operationalizations facing a validity argument.

3. **Dell & Rambachan (2026).** NBER SI Methods Lecture, 30 Jul 2026, *Estimation and Inference with AI-Generated Data.* [3]
   Field-leader translation of nomological-network logic into PI language; explicit call for “principled, widely accepted methods for construct validity.” **Gap:** lecture, not an operational menu-level selection rule. (Slide-level quotes previously verified 2026-08-09 against `dell4.pdf`; not re-extracted this session — NBER cookie wall.)

4. **Rambachan & Roth (2023).** *A More Credible Approach to Parallel Trends.* RESTUD. DOI 10.1093/restud/rdad018. [4][5]
   Causal parameter partially identified under restrictions on how post-treatment PT violations can differ from pre-trends. **Gap:** identification of a *treatment effect*, not of a measurement. This is the downstream demo, not a competitor to M*.

5. **Cronbach & Meehl (1955).** *Construct validity in psychological tests.* Psych Bulletin. DOI 10.1037/h0040957. [9]
   Nomological network. **Gap:** no set-valued inference, no admissible menu, no propagation into β.

6. **Simonsohn, Simmons & Nelson (2020)** specification curve [10]; **Steegen et al. (2016)** multiverse [11].
   Enumerate analyst degrees of freedom and report a distribution. **Gap:** every specification gets a vote. No validity filter before the range.

7. **Bean et al. (2025).** *Measuring what Matters.* NeurIPS D&B; arXiv:2511.04703. [12]
   445 LLM benchmarks, 29 reviewers, 8 recommendations. **Gap:** benchmark-*design* validity, not menu-level admission.

8. **Freiesleben (2026).** *Establishing Construct Validity in LLM Capability Benchmarks Requires Nomological Networks.* arXiv:2603.15121. [13]
   Philosophical case that nomological networks are the right account for LLM capabilities. **Gap:** non-formal; no M*, no [L,U], no software.

**Phrase search.** `"construct-identified inference"` / `"construct identified inference"` returns only the author’s own Substack [6] and EconLLM Lab page [8]. Naming is unique. Method is not.

**Software.** `cvprofiles` 3.0.2 is live on PyPI [7]. No competing package implementing nomological-restriction admission over a measurement menu was found this session (search was not exhaustive of PyPI).

## 2. Novelty verdict

**The exact conjunction was not found in print.** Every component exists separately.

Decompose:

| Piece | Status |
|---|---|
| Construct validity / nomological networks | 1955, crowded |
| Partial identification | Manski lineage; 2026 boom in LLM-measurement PI |
| Spec curve / multiverse | 2016–2020, now routine robustness |
| PI of β over multiple measurements | Ogut–Yin 2026, same destination |
| PI from LLM prompts | Chen–Rambachan–Tamer 2026 |
| Nomological networks as identifying structure (argument) | Dell–Rambachan lecture; Freiesleben |
| **Finite menu + restriction tests → M* + [L,U](β \| M*) + holdout-falsifiable selection + software** | **not found** |

**Minimal novel core that survives attack:** operationalizing construct validity as *set-valued inference over a researcher-owned restriction-tested menu*, with empty M* as a designed finding, and a released engine. Keep it that narrow.

**What a reviewer attacks:**
1. Degrees of freedom relocated: who audits θ / the restriction set?
2. Data-dependent admission = pretesting / selection; holdout is the answer, and it has to actually bind.
3. Mandatory contrast with Ogut–Yin (same [L,U] destination) and CRT (same PI-of-measurement neighborhood).
4. Knife-edge thresholds; empty-set vs rescued-set.
5. Unpublished paper; software is existence proof, not a scientific claim.
6. Flagship (WVS/GPS patience) is deliberately modest.

**On the three labels the user offered:**

- **Novel approach I can claim** — only the conjunction, never the pieces. “We invented construct validity” / “we invented partial identification of measurement” are false.
- **Pioneering** — no. Dell, Rambachan, Tamer, Chen, Cronbach–Meehl, Manski, Ogut–Yin pioneered the pieces. The honest social claim is *early operationalization of a gap the field’s leaders named in 2026*.
- **Minority of adopters** — yes, and this is the only of the three that is currently safe on a consulting page. Spec-curve robustness is common; restriction-tested admission of a measurement menu is not.

## 3. Named paper

No third-party paper titled “construct-identified inference.” The name is the author’s (Substack, 30 Aug 2026). [6]

## 4. Recency caveat

arXiv API 429’d this session on search queries. Recency sweep after 2026-08-10 is incomplete; CRT and Ogut–Yin abs pages were re-extracted live. A paper landing in Aug–Sep 2026 that does the conjunction would change the verdict.
