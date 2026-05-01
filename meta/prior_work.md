# Prior Work — Safety Criteria as the Independent Variable

## The literature gap this paper fills

LLM safety has accumulated a *zoo* of benchmarks since 2018 — over 102
public benchmarks per the 2024 survey, with ~ 12 used in evaluating
state-of-the-art frontier models. Each measures a different facet:
helpfulness, harmlessness, honesty, refusal calibration, jailbreak
resistance, bias, toxicity, regulatory-risk coverage. Yet:

> **No paper has reported the pairwise reversal-rate matrix between
> these safety metrics, with bootstrap CIs, on a fixed set of frontier
> LLMs.**

The literature is rich on each individual axis and on holistic
*aggregations*, but the **case-level question** — "if I switch from
HarmBench to AIR-Bench, does my model's safety ranking flip?" — is
unanswered as a pre-registered statistical claim.

We import the criterion-as-independent-variable framework, validated
on LLM Q&A (paper 3, criteria-iv-experiment, NeurIPS E&D submission),
finance ranking (paper 5, finance-criteria-iv-experiment), and
text-to-image evaluation (paper 7, image-criteria-iv-experiment), and
apply it to LLM safety.

## Three traditions

### Tradition 1 — Holistic safety evaluation (Stanford CRFM)

- **HELM Safety** (Stanford, Liang et al. 2024) — multi-metric × multi-
  model evaluation framework. Reports aggregate scores and per-metric
  rankings. Acknowledges qualitative disagreement
  ("no single model excels in all aspects") but does not provide
  pair-flip statistics.
- **AIR-Bench 2024** (Zeng et al. 2024) — regulation-grounded safety
  taxonomy (8 government regulations, 16 company policies, 314 risk
  categories, 5694 prompts). Scores integrated into HELM.
- **HHH** (Anthropic, Askell et al. 2021) — original Helpfulness/
  Honesty/Harmlessness preference dataset.

These works **measure** but do not **statistically test** cross-metric
disagreement.

### Tradition 2 — Per-axis benchmarks

- **HarmBench** (Mazeika et al. 2024) — adversarial prompt corpus,
  reports Attack Success Rate.
- **JailbreakBench / AdvBench** — jailbreak resistance.
- **SORRY-Bench** / **SORRY-Bench 2** (ICLR 2025) — refusal-rate
  calibration; explicitly notes that aggressive defenses inflate
  false-refusal rates and undermine usability.
- **BEAVERTAILS** (Ji et al. 2023) — disentangled human-preference
  data for harmlessness vs helpfulness; the paper itself notes that
  "helpfulness judgment can be distinctly different from the
  harmlessness judgment."
- **TruthfulQA** (Lin et al. 2022) — truthfulness vs informativeness.
- **StereoSet, BBQ, ToxiGen, RealToxicityPrompts** — bias/toxicity.
- **AlpacaEval / WildBench** — helpfulness Elo.

Each benchmark documents a single failure mode. **None reports** how
its rankings interact with other safety benchmarks at the pair level.

### Tradition 3 — Safety/usability trade-off (qualitative)

- **Bai et al. (2022)**, *Constitutional AI*, formalises the helpfulness
  vs harmlessness tension qualitatively.
- **Cui et al. (2025)**, *LLM Alignment should go beyond Harmlessness–
  Helpfulness*, argues that the two-axis tradeoff is itself an
  oversimplification; human agency matters as a third axis.
- **The Scales of Justitia** (Liu et al. 2025), comprehensive survey
  of safety evaluation, identifies fragmentation but proposes
  taxonomy, not statistical test.

These works **frame** the disagreement but **do not quantify** it.

### Tradition 4 — Ranking-stability literature (general ML eval)

- **Re-evaluating Automatic LLM System Ranking** (Findings NAACL 2025)
  — uses bootstrap mean ± 95 % CI on ranking correlations between
  pairwise automatic and human evaluations. Spearman ρ = 0.93 between
  Llama-3.1-70B BT-aggregated pairs and human annotators, but
  ranking correlation degrades on close-performing systems.
- **Aligning with Human Judgement** (ICLR 2024, Liu et al.), pairwise
  preference for LLM evaluator alignment.
- **JADES** (2025), jailbreak assessment via decompositional scoring.

Methodologically close, but **focused on judge-vs-human** alignment,
not **safety-metric-vs-safety-metric** ranking reversal.

## The gap, summarised

| Tradition | What it does | What it does not do |
|---|---|---|
| 1. Holistic safety (HELM, AIR-Bench) | multi-metric tables + qualitative claims | pair-flip statistics, bootstrap CI |
| 2. Per-axis benchmarks | depth on one axis | cross-axis interaction |
| 3. Helpfulness vs harmlessness framing | qualitative tradeoff | systematic statistical test |
| 4. Ranking stability | judge ↔ human ranking correlation | safety-metric ↔ safety-metric reversal rate |

## What we do

1. **Collect public scores** from the major safety leaderboards
   (HELM Safety, AIR-Bench, HarmBench, AdvBench, SORRY-Bench,
   AlpacaEval helpfulness, WildBench, JailbreakBench, plus selected
   honesty/bias benchmarks).
2. **Build an 8-12 LLM × 8-10 metric matrix** of frontier-model scores.
3. **Apply the criterion-as-IV statistical pipeline** (paper 7's
   instrument):
   - Pairwise reversal rate (within-set image-pair generalisation:
     for safety, within-LLM-pair, across criteria)
   - Bootstrap CI (B = 1000) over LLMs (cluster bootstrap if needed)
   - Spearman ρ + Kendall τ matrix
   - Hierarchical clustering of metrics on (1 − ρ)
4. **Cross-reference structure**:
   - Helpfulness-class metrics vs harmlessness-class
   - Within-axis metric-pair reversal (HarmBench vs AdvBench)
   - Across-axis metric-pair reversal (HarmBench vs AlpacaEval)
5. **Headline question**: of the C(N, 2) metric pairs we examine, how
   many produce > 30 % reversal in LLM ranking?

## Pre-registered hypotheses

- **H1 (case-level disagreement).** ≥ 1 metric pair has reversal rate
  ≥ 30 % with bootstrap CI lower bound > 25 %.
- **H2 (Spearman ρ alone is misleading).** ≥ 1 metric pair has
  ρ ≥ 0.50 *and* reversal rate ≥ 25 %.
- **H3 (cluster structure).** ≥ 2 distinct clusters appear,
  separating helpfulness-class metrics from harmlessness-class
  metrics.
- **H4 (within-axis vs across-axis).** Within-axis pairs (e.g.,
  HarmBench ↔ AdvBench, both jailbreak/harmfulness) have lower
  reversal rates than across-axis pairs (e.g., HarmBench ↔ AlpacaEval),
  with statistical separation.
- **H5 (consistency with the criteria-IV programme).** The
  qualitative pattern matches paper 3 (LLM Q&A) and paper 7 (T2I):
  ρ ≥ 0.5 pairs still flip on ≥ 25 % of LLM pairs.

The paper is interesting in either direction. Falsification of any
single H refines the framework; falsification of all five would
genuinely surprise (and we would investigate why safety differs
from Q&A and T2I).

## Anchoring citations

1. Liang, P. et al. (2024). *HELM: Holistic evaluation of language
   models.* TMLR.
2. Zeng, Y. et al. (2024). *AIR-Bench 2024: A safety benchmark
   based on risk categories from regulations and policies.* arXiv
   2407.17436.
3. Mazeika, M. et al. (2024). *HarmBench: A standardized evaluation
   framework for automated red teaming and robust refusal.* ICML.
4. Lin, S., Hilton, J. & Evans, O. (2022). *TruthfulQA: Measuring how
   models mimic human falsehoods.* ACL.
5. Bai, Y. et al. (2022). *Training a helpful and harmless assistant
   with reinforcement learning from human feedback.* arXiv
   2204.05862.
6. Bai, Y. et al. (2022). *Constitutional AI.* arXiv 2212.08073.
7. Ji, J. et al. (2023). *BEAVERTAILS: Towards improved safety
   alignment of LLM via a human-preference dataset.* NeurIPS.
8. Liu, S. et al. (2025). *The scales of justitia: A comprehensive
   survey on safety evaluation of LLMs.* arXiv 2506.11094.
9. Cui, Y. et al. (2025). *LLM Alignment should go beyond
   Harmlessness–Helpfulness and incorporate Human Agency.*
   Cognitive Computation.
10. JADES collaborators (2025). *JADES: A universal framework for
    jailbreak assessment via decompositional scoring.* arXiv
    2508.20848.
11. SORRY-Bench 2 (ICLR 2025).
12. Re-evaluating Automatic LLM System Ranking (Findings NAACL 2025).
13. paper 3: criteria-iv-experiment (NeurIPS E&D submission, present
    authors). **Methodology source.**
14. paper 5: finance-criteria-iv-experiment (companion submission).
15. paper 7: image-criteria-iv-experiment (companion submission).

## Connection to companion papers

| Paper | Domain | Data type | This paper's relation |
|---|---|---|---|
| paper 3 (NeurIPS E&D) | LLM Q&A eval | text | **methodology source** |
| paper 4 (TMLR) | LLM agents | text | unrelated |
| paper 5 (companion) | Finance fund ranking | time-series | sister, criteria-IV in finance |
| paper 6 (companion) | Radiology AI | imaging | unrelated |
| paper 7 (companion) | T2I evaluation | image+text | **direct sister, criteria-IV in image** |
| paper 7-archive (semicon) | Manufacturing | tabular | unrelated |
| paper 9-archive (finance Confirmation) | Finance trading | time-series | unrelated |
| paper 10 (failure-modes) | Confirmation scope | meta | unrelated |
| **this paper** | **LLM safety** | **text** | **fourth criteria-IV instance** |

## What this paper is *not* claiming

- Safety benchmarks are *all wrong*. Each measures something real on
  its own axis. Our claim is that the field has been treating these
  axes as if they were one quantity ("safety SOTA") when they are not.
- Helpfulness *is* harmless. Bai et al. (2022) showed the trade-off
  exists. Our contribution is to **quantify how often** it produces
  ranking flips, not to discover that flips can occur.
- A single "best safety metric" exists. The point of the
  criterion-as-IV framework is that there is no such thing; the choice
  of metric is itself a research-design variable.

## Why this paper

- **Cost**: ~ 2-3 weeks
- **Compute**: zero new evaluation runs (we aggregate public
  leaderboard scores)
- **Risk**: low — ample empirical evidence of disagreement
  exists qualitatively; we operationalise the case-level statistic
- **Venue match**: TMLR primary (long-format, rolling); NeurIPS 2026
  Workshop on Trustworthy ML alternative
- **Generality argument**: fourth cross-domain validation of the
  criterion-as-IV framework (LLM Q&A → finance → T2I → safety)
