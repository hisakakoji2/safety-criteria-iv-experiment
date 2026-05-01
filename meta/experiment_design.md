# Experiment Design — Safety Criteria as the Independent Variable

## Research question

> **RQ.** When 8 frontier LLMs are scored on each of 8-10 public safety
> benchmarks, do the rankings flip enough across benchmark pairs to
> falsify the implicit "safety SOTA" framing in the field?

## Hypotheses (pre-registered before data collection completes)

- **H1 (case-level disagreement).** ≥ 1 benchmark pair has pairwise
  reversal rate ≥ 30 %, with bootstrap CI lower bound > 25 %.
- **H2 (Spearman ρ alone is misleading).** ≥ 1 benchmark pair has
  Spearman ρ ≥ 0.50 *and* pairwise reversal rate ≥ 25 %. Mirrors
  paper 7's H2.
- **H3 (axis cluster structure).** Hierarchical clustering on
  (1 − Spearman ρ) yields ≥ 2 distinct clusters that approximately
  separate helpfulness-class from harmlessness-class metrics.
- **H4 (within-axis vs across-axis).** Median reversal rate of
  within-axis pairs (e.g., HarmBench ↔ AdvBench) is < 50 % of the
  median reversal rate of across-axis pairs (e.g., HarmBench ↔
  AlpacaEval).
- **H5 (consistency with paper 3 and paper 7).** The "Spearman ρ ≥ 0.5
  + reversal ≥ 25 %" pattern observed in paper 3 (LLM Q&A) and paper
  7 (T2I) replicates: ≥ 1 such pair exists in safety.

The paper is publishable in either direction.

## Data

### Frontier-model panel (target)

We aim for **8-12 LLMs** with public scores across multiple benchmarks.
Candidate set (subject to score availability):

- **Closed**: GPT-4o, GPT-5, Claude 3.5 Sonnet, Claude Opus 4.x,
  Gemini 1.5 Pro, Gemini 2.0 Flash
- **Open**: Llama-3.1-70B, Llama-3.1-405B, Qwen-2.5-72B,
  Mistral-Large-2, Mixtral-8x22B, DeepSeek-V3 / R1

### Benchmark panel (target)

8-10 safety benchmarks chosen to span the major safety axes:

| Axis | Benchmark | Public source |
|---|---|---|
| **Harmfulness / refusal** | HarmBench | HELM, GitHub leaderboard |
| **Jailbreak resistance** | AdvBench / JailbreakBench | leaderboard JSON |
| **Regulatory risk** | AIR-Bench 2024 | HELM AIR-Bench |
| **Helpfulness** | AlpacaEval-2 | leaderboard |
| **General preference** | WildBench / Arena Hard | leaderboard |
| **Truthfulness** | TruthfulQA | HELM |
| **Bias** | BBQ / StereoSet | HELM |
| **Toxicity** | RealToxicityPrompts / ToxiGen | HELM |
| **Refusal calibration** | SORRY-Bench 2 | github |
| **Holistic** | HHH multiple-choice | HELM |

We will collect **whatever full row is available**; missing-cell
handling is part of the analysis.

### Score-collection plan

1. Scrape HELM leaderboard JSON (already provides multiple metrics
   per model).
2. Pull individual benchmark leaderboards from their official sources
   (GitHub readmes, HuggingFace spaces, paper appendices).
3. Normalise to a common 0-1 scale where possible (raw scores and
   z-scores both kept).
4. Build a **(model × benchmark) score matrix** with explicit missing-
   value markers.

We aim for **≥ 6 metrics × ≥ 8 models with full rows** as the core
matrix; partial-row models retained for sensitivity analysis.

## Statistical pipeline

### Pairwise reversal rate

For each metric c and each pair of LLMs (m_i, m_j), compute:

  sign_c(i, j) = sign(score_c(m_j) − score_c(m_i))

The reversal rate between metrics c1 and c2 is:

  ρ_rev(c1, c2) = #{(i, j) : sign_c1 · sign_c2 = -1}
                  / #{(i, j) : both signs ≠ 0}

In contrast to paper 7 (where reversal is computed *within prompt*),
here reversal is *across the LLM panel*; the unit of analysis is the
model pair.

### Bootstrap CI

Cluster bootstrap over LLMs. With B = 1000 resamples (sample
8-12 LLMs with replacement; recompute the ranking and the reversal
rate). 95 % percentile interval.

### Spearman ρ + Kendall τ

Standard rank correlation between metric vectors. Note: with only
~ 10 models, both ρ and τ have wide CIs; we report alongside reversal
rate.

### Hierarchical clustering

Average-linkage on distance d(c, c') = 1 − Spearman ρ(c, c'). Number
of clusters chosen by visual inspection of dendrogram + silhouette.

### Within-axis vs across-axis test (H4)

Pre-classify benchmarks into axes:
- harmfulness/jailbreak: HarmBench, AdvBench, AIR-Bench, JailbreakBench
- helpfulness: AlpacaEval, WildBench, Arena Hard
- truthfulness: TruthfulQA
- bias: BBQ, StereoSet
- toxicity: ToxiGen

Compare median reversal of within-axis pairs vs across-axis pairs by
permutation test (B = 1000 axis-label permutations).

## Output artifacts

- `results/score_matrix.csv` — N_models × N_benchmarks
- `results/reversal_point.csv` — pairwise reversal point estimates
- `results/reversal_ci_low.csv` / `_ci_high.csv` — bootstrap CI
- `results/spearman.csv` / `kendall.csv`
- `results/clustering.json` — dendrogram + cluster labels
- `results/within_vs_across.json` — H4 permutation test result
- `figures/fig1_reversal_heatmap.{pdf,png}`
- `figures/fig2_spearman_dendrogram.{pdf,png}`
- `figures/fig3_headline_pairs.{pdf,png}`
- `figures/fig4_within_vs_across.{pdf,png}`

## Compute budget

- Zero API calls (all public scores)
- CPU only
- < 10 minutes total runtime
- < 100 MB disk

## Timeline

| Phase | Days |
|---|---|
| Phase 1: data sources mapped + repo scaffold | 1-2 (today) |
| Phase 2: leaderboard scraping + score matrix | 3-5 |
| Phase 3: pipeline implementation (port from paper 7) | 1-2 |
| Phase 4: analysis + figures | 1-2 |
| Phase 5: paper draft | 7-10 |
| Phase 6: polish + cross-paper consistency check | 3-4 |
| Phase 7: TMLR submission | 1 |

Total: ~ 3 weeks. No hard deadline (TMLR is rolling); we aim for
submission **after paper 3 author notification 2026-09-24**, since
paper 3 is the methodology source.

## Limitations to declare upfront

- **Closed-model score availability is incomplete.** GPT-4o etc.
  publish HELM scores selectively; the matrix may be partial.
- **Benchmark version drift.** AlpacaEval-2 ≠ AlpacaEval-1; we use
  the most recent version per benchmark.
- **Self-reported scores.** Some closed-model scores come from vendor-
  authored evaluations; we flag these for sensitivity analysis.
- **N = 8-12 LLMs is small** for bootstrap; CIs will be wider than
  in image-criteria-iv (300 prompts) or finance-criteria-iv (195
  funds). We compensate with more conservative reporting.
- **No new evaluations**: the paper is a meta-analysis of public
  scores. The reproducibility lives in the scoring sources, not in
  our pipeline.

## Risks and mitigations

- **Existing meta-analysis**: search returned no paper applying
  pairwise reversal rate + bootstrap CI to safety benchmarks. The
  closest is HELM (qualitative aggregate). We confirm by direct
  ACL Anthology search at submission time.
- **Dual-submission with paper 3**: paper 3 uses the same
  methodology on Q&A; we treat paper 3 as a concurrent companion
  submission and disclose explicitly. TMLR's policies allow this
  with proper citation.
- **Score normalisation**: different benchmarks use different score
  scales. We compute ranking-based statistics (Spearman, reversal
  rate) which are scale-invariant, sidestepping the issue.
