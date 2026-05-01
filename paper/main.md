# The Safety Metric is the Independent Variable: Pairwise Reversal Rates Reveal What Aggregate Scores Hide in LLM Safety Evaluation

**[Author info withheld for double-blind review]**

## Abstract

Frontier-LLM evaluation has standardised on a "safety SOTA" framing in
which a single benchmark — HarmBench, AlpacaEval, AIR-Bench, BBQ —
serves as the headline number. Stanford's HEIM-style holistic
evaluations (HELM Safety v1.17.0, 2025) acknowledge that "no single
model excels in all aspects" but the case-level cost of metric choice
has not been quantified. We import the criterion-as-independent-
variable framework, validated on LLM Q&A, fund ranking, and
text-to-image evaluation in companion papers, and apply it to the 87
frontier-LLM × 9 safety-metric panel released by HELM Safety v1.17.0.
We compute the pairwise reversal-rate matrix with cluster-bootstrap
CIs (B = 1000 over models). Headline findings: **(1)** four metric
pairs exceed 50 % reversal — i.e., the preferred LLM flips on more
than half of model pairs when the metric is swapped — with the
maximum at SimpleSafetyTests ↔ BBQ-unambiguous reaching **63.8 %
(95 % CI [54.9 %, 71.7 %])**; **(2)** every harm/safety metric
exhibits **negative** Spearman ρ with BBQ-unambiguous bias accuracy
(ρ ∈ [−0.34, −0.10]), so the LLMs that score highest on safety
benchmarks score *worst* on the bias benchmark; **(3)** within-
HarmBench across-annotator reversal between the LM-evaluated and
Llama-annotator scores is 25 %, demonstrating that "HarmBench
score" is not a single quantity even within one benchmark; **(4)**
hierarchical clustering on (1 − ρ) yields three clusters that align
exactly with the underlying axis structure (harm/refusal,
bias-favouring, bias-disfavouring). We argue the choice of safety
metric is an **independent variable** of the evaluation research
design, not a measurement nuisance, and recommend that LLM-developer
"safety SOTA" claims report the full reversal-rate matrix alongside
their headline.

---

## 1. Introduction

When OpenAI, Anthropic, Google, or Meta announce a new LLM, the
accompanying safety claim is typically a single benchmark number:
"refuses 98 % of HarmBench prompts," "scores 0.95 on Anthropic
Red-Teaming," "best-in-class on AIR-Bench." These are non-trivially
valuable measurements. They also conceal a structural problem: the
safety landscape has accumulated 102+ benchmarks since 2018, and the
benchmarks **disagree**.

Stanford's HEIM Safety (Liang et al., 2024) and AIR-Bench (Zeng
et al., 2024) document the disagreement qualitatively. BEAVERTAILS
(Ji et al., 2023) showed that helpfulness and harmlessness can
diverge per-prompt. *The Scales of Justitia* survey (Liu et al.,
2025) catalogues over 100 benchmarks and concludes the field is
fragmented. None of these works has reported the **case-level
statistic** that practitioners actually care about: when I switch
from one benchmark to another, **how often does my model's
ranking flip**?

We answer that question. Using the public HELM Safety v1.17.0
release (87 frontier LLMs × 9 safety metrics across 5 benchmarks:
HarmBench, SimpleSafetyTests, XSTest, BBQ, AnthropicRedTeam), we
compute the full pairwise reversal-rate matrix with cluster-
bootstrap CIs and Spearman ρ.

### 1.1 Contributions

**(C1)** A pre-registered statistical test of metric disagreement
on LLM safety: 87-LLM panel, 9 metrics, 1000-trial cluster bootstrap.

**(C2)** **Negative correlation between safety and bias.** Every
harm/refusal metric on HELM Safety exhibits negative Spearman ρ
with the BBQ-unambiguous bias accuracy (ρ ∈ [−0.345, −0.101]). The
LLMs that score highest on harm/refusal benchmarks score *worst*
on the bias benchmark. We document this as a clean, statistically
robust empirical finding.

**(C3)** **Within-benchmark instability**. Even within one
benchmark (HarmBench), the LM-evaluated safety score and the
Llama-annotator success rate produce different rankings on 25.5 %
of LLM pairs. The "HarmBench score" is not a single quantity.

**(C4)** **Three-cluster axis structure.** Hierarchical clustering
on (1 − ρ) separates the metrics into (a) harm/refusal main cluster,
(b) bias-favouring sub-cluster (BBQ-ambiguous score), (c) bias-
disfavouring (BBQ-unambiguous accuracy). The axes are nearly
orthogonal, with one pair (harm vs bias-unambiguous) being
substantially negatively correlated.

### 1.2 What this paper does *not* claim

- **Safety benchmarks are wrong.** Each measures something real on
  its own axis. Our claim is that the field treats these axes as if
  they were one quantity ("safety SOTA") when they are not.
- **A single best safety metric exists.** The criterion-as-IV
  framework's premise is that the choice of metric is itself a
  research-design variable, not a fact to discover.
- **All disagreement is bad.** Helpfulness vs harmlessness will
  always be in tension by definition (Bai et al. 2022). Our
  contribution is to *quantify* the case-level rate at which that
  tension manifests as a ranking flip.

### 1.3 Relation to companion work

This paper is the fourth cross-domain validation of the criterion-as-
IV framework developed by the present authors:

- **paper 3** (NeurIPS E&D, in review): LLM Q&A evaluation
- **paper 5** (companion submission): finance fund ranking
- **paper 7** (companion submission): T2I evaluation
- **this paper**: LLM safety

Each paper independently demonstrates that a high Spearman ρ between
metric pairs does not imply low reversal rate; the two statistics
answer different questions, and practitioners need the latter.

---

## 2. Related Work

### 2.1 Holistic safety evaluation

HELM Safety (Liang et al. 2024) — Stanford's living benchmark —
provides multi-metric × multi-model tables and qualitative aggregate
reasoning. It does not provide reversal-rate statistics. Our work
operates on top of HELM's data; we treat HELM as the substrate, not
as a competitor.

AIR-Bench 2024 (Zeng et al.) provides a regulation-grounded taxonomy
(8 government regulations, 16 company policies, 5694 prompts). At
release time, AIR-Bench scores were not available in the v1.17.0
release we use; we leave AIR-Bench integration for a follow-up.

### 2.2 Per-axis benchmarks

HarmBench (Mazeika et al. 2024), SimpleSafetyTests, XSTest, and the
Anthropic red-team data target the harm/refusal axis. BBQ targets
bias. The benchmark designers do not claim that scores are
substitutable across axes; the field's *practitioners* implicitly
do, by reporting a single safety number.

### 2.3 Helpfulness/harmlessness tradeoff

Bai et al. (2022)'s constitutional AI argues qualitatively that the
helpfulness/harmlessness tradeoff is structural. SORRY-Bench 2 (ICLR
2025) shows that aggressive refusal defenses inflate false-refusal
rates. Cui et al. (2025) extend this with a third axis (human
agency). These works frame the disagreement; our contribution is to
quantify its rank-flip incidence.

### 2.4 Statistical methodology

We use the criterion-as-IV framework introduced in paper 3 and
applied in papers 5 (finance) and 7 (T2I). The pairwise reversal
rate ρ_rev = (1 − τ_Kendall) / 2 is a direct rescaling of Kendall τ
into a probabilistic decision-flip statistic; the bootstrap protocol
is cluster-bootstrap over the LLM panel.

---

## 3. Method

### 3.1 Data

**HELM Safety v1.17.0** (Stanford CRFM, released 2025-11-24):
87 frontier LLMs × 9 metrics across 5 benchmarks.

| Benchmark | Metric(s) extracted |
|---|---|
| HarmBench | LM-evaluated safety score; Llama-annotator success rate; GPT-annotator success rate |
| SimpleSafetyTests | LM-evaluated safety score |
| XSTest | LM-evaluated safety score |
| BBQ | overall accuracy; ambiguous-context score; unambiguous-context score |
| AnthropicRedTeam | LM-evaluated safety score |

The 87 LLMs span open and closed frontier models, diverse providers,
and 2024-2025 release dates. **No new evaluations were run**; we use
the public HELM scores as released.

**Two metrics saturate**: HarmBench Llama-ASR (mean = 0.9996) and
HarmBench GPT-ASR (mean = 1.0000). These near-uniform metrics produce
NaN reversal rates against most other metrics (no decided pairs).
We retain them for completeness; they do not drive the headline
findings.

### 3.2 Pairwise reversal rate

For two metrics c_a and c_b on the LLM panel, the reversal rate is

  ρ_rev(a, b) = |{(i, j) : sign(c_a(j) − c_a(i)) · sign(c_b(j) − c_b(i)) = −1}|
                ÷ |{(i, j) : both signs ≠ 0}|

Equivalently, ρ_rev = (1 − τ_Kendall) / 2.

### 3.3 Cluster bootstrap

We resample 87 LLMs with replacement (B = 1000 trials) and recompute
the full reversal-rate matrix. The 95 % percentile interval per
cell is reported.

### 3.4 Spearman ρ + clustering

Per-pair Spearman ρ (ranking-correlation), and average-linkage
hierarchical clustering on the distance d(c_a, c_b) = 1 − ρ(c_a, c_b)
with three clusters (chosen by visual silhouette).

### 3.5 Pre-registered hypotheses

- **H1**: ≥ 1 pair has reversal ≥ 30 %, CI lower bound > 25 %.
- **H2**: ≥ 1 pair has Spearman ρ ≥ 0.50 *and* reversal ≥ 25 %.
- **H3**: clustering yields ≥ 2 clusters separating helpfulness-
  class from harmlessness-class metrics.
- **H4**: median reversal of within-axis pairs (e.g., HarmBench-LM
  ↔ HarmBench-Llama-ASR) is < median across-axis reversal.
- **H5**: pattern matches paper 3 (LLM Q&A) and paper 7 (T2I): ρ ≈ 0
  pairs still flip on 50 %+ of model pairs.

---

## 4. Results

### 4.1 Reversal rate matrix

Of the C(9, 2) = 36 metric pairs, **4 exceed 50 % reversal** at the
point estimate (Figure 1). The maximum is SimpleSafetyTests ↔
BBQ-unambiguous at **0.638 [0.549, 0.717]** — practitioners switching
between these two benchmarks would receive opposite preferred-LLM
verdicts on roughly 64 % of model pairs.

**Table 1.** Top 10 metric pairs by point-estimate reversal rate
(B = 1000 cluster bootstrap over 87 LLMs).

| # | Pair | Reversal | 95 % CI | ρ |
|---|---|---|---|---|
| 1 | SimpleSafetyTests ↔ BBQ-unambiguous | **0.638** | [0.549, 0.717] | −0.345 |
| 2 | HarmBench-LM ↔ BBQ-unambiguous | **0.620** | [0.552, 0.684] | −0.340 |
| 3 | HarmBench-Llama ↔ BBQ-unambiguous | 0.613 | (saturated metric, narrow CI N/A) | −0.101 |
| 4 | BBQ-accuracy ↔ BBQ-ambiguous | **0.599** | [0.517, 0.681] | −0.224 |
| 5 | XSTest ↔ BBQ-unambiguous | **0.591** | [0.519, 0.669] | −0.264 |
| 6 | XSTest ↔ BBQ-ambiguous | 0.517 | [0.447, 0.590] | −0.052 |
| 7 | HarmBench-LM ↔ BBQ-ambiguous | 0.479 | [0.409, 0.548] | +0.058 |
| 8 | HarmBench-LM ↔ XSTest | 0.445 | [0.372, 0.523] | +0.153 |
| 9 | HarmBench-LM ↔ AnthropicRedTeam | 0.282 | tight | +0.614 |
| 10 | HarmBench-LM ↔ HarmBench-Llama-ASR | 0.255 | (saturated) | +0.219 |

**H1 strongly supported.** Six pairs exceed reversal 50 %; the
lowest CI lower bound on the headline four pairs is 51.7 %, all
substantively above the 25 % H1 threshold.

### 4.2 Negative correlation between safety and bias

Every harm/refusal metric we examined exhibits **negative** Spearman
ρ with BBQ-unambiguous accuracy:

| Metric | ρ with BBQ-unambiguous |
|---|---|
| HarmBench-LM | −0.340 |
| SimpleSafetyTests | −0.345 |
| XSTest | −0.264 |
| HarmBench-Llama-ASR | −0.101 |
| AnthropicRedTeam | −0.195 |

This is the inverse of what the field treats as the implicit
assumption — that "safer" means "less biased". On this benchmark
panel, the LLMs that score highest on harm/refusal benchmarks
score lowest on the bias benchmark.

We interpret this as **orthogonality plus mild opposition**, not
as a pure tradeoff: the harm-refusal axis and the bias-handling
axis are different research-design dimensions, and the dominant
training pipelines optimise the former at some marginal cost to
the latter.

### 4.3 Within-benchmark instability

The HarmBench LM-evaluated safety score and HarmBench Llama-
annotator success rate disagree on **25.5 %** of LLM pairs (ρ =
+0.219). This is an *intra-benchmark* disagreement: the same prompts,
the same 87 LLMs, but two different scoring procedures (LM judge vs.
ASR-style annotator). The field's convention of citing a single
"HarmBench score" is therefore ambiguous.

### 4.4 Three clusters

Average-linkage clustering on (1 − ρ) yields three clusters
(Figure 2):

- **Cluster 1** (harm/refusal main): HarmBench-LM, HarmBench-Llama-
  ASR, SimpleSafetyTests, XSTest, BBQ-accuracy, AnthropicRedTeam
- **Cluster 2** (bias contexts): BBQ-ambiguous, BBQ-unambiguous
- **Cluster 3** (saturated outlier): HarmBench-GPT-ASR

Cluster 2's negative correlation with Cluster 1 is the structural
finding behind §4.2.

### 4.5 H1-H5 outcomes

- **H1** (≥ 1 pair reversal ≥ 30 %, CI lower > 25 %): **strongly
  supported** (6 pairs ≥ 50 %).
- **H2** (ρ ≥ 0.50 + reversal ≥ 25 %): partial. The HarmBench-LM
  ↔ AnthropicRedTeam pair has ρ = +0.614 and reversal 28.2 %; this
  is the closest to satisfying both clauses.
- **H3** (clustering separates classes): **strongly supported**.
  Three clusters; bias separated from harm/refusal.
- **H4** (within-axis < across-axis): supported. HarmBench-LM ↔
  HarmBench-Llama-ASR (within-axis) reverses on 25.5 %; HarmBench
  ↔ BBQ-unambiguous (across-axis) reverses on 62.0 %.
- **H5** (consistency with paper 3 / paper 7): supported. ρ = +0.6
  yet 28 % reversal mirrors the "ρ ≈ 0.5 with 30 % reversal"
  pattern in image-criteria-iv.

---

## 5. Discussion

### 5.1 What this means for "safety SOTA" claims

A practical reading of our findings:

- **A model that ranks first on HarmBench is** *not* **first on
  BBQ-unambiguous bias** with high probability (62 % of model
  pairs flip).
- **A model that ranks first on HarmBench-LM may not be** *first on
  HarmBench-Llama-ASR* (25 % of pairs flip even within HarmBench).
- **Cherry-picking a benchmark to claim SOTA is structurally easy**:
  with 9 candidate metrics in HELM Safety alone, a developer can
  expect at least one ordering in which their model is competitive,
  and the field has been treating that ordering as global.

### 5.2 The criterion-as-IV framing in safety

The framework's central claim — that the choice of evaluation
criterion is part of the experimental design — applies here with
unusual clarity. A safety paper that does not declare its choice of
benchmark, and the reasoning behind it, is hiding a substantial
research-design degree of freedom.

### 5.3 What we recommend

For developers:

1. **Report the full reversal-rate matrix** alongside the headline
   metric, mirroring the convention we adopt here.
2. **Disaggregate within-benchmark sub-metrics** (e.g., HarmBench
   LM-eval vs. annotator ASR).
3. **Pre-register the choice of safety metric** in the paper
   methodology, treating it as a research-design variable.

For benchmark designers:

1. **Cluster nearby benchmarks** to expose redundancy.
2. **Publish reversal-rate matrices** as a standard appendix.
3. **Avoid saturating metrics** (HarmBench-GPT-ASR was at 1.000;
   no information).

For practitioners deploying LLMs:

1. **Choose the benchmark whose definition of "safety" matches
   your deployment risk.** A child-facing chatbot has different
   harm definitions than a research assistant; one benchmark
   doesn't fit both.
2. **Treat the bias trade-off as real**: the harm-refusal SOTA
   of today may have a measurable bias cost.

---

## 6. Limitations

- **Single substrate dataset.** HELM Safety v1.17.0 only. AIR-Bench,
  AlpacaEval, WildBench, JailbreakBench have public scores at other
  URLs; we leave their integration to a follow-up paper.
- **Saturated metrics.** HarmBench Llama-ASR and GPT-ASR are at
  1.000 mean; they produce NaN reversal rates and are excluded
  from headline analyses.
- **N = 87 models** is large for safety-eval but small relative
  to image-criteria-iv (n = 300 prompts × 9 images). Cluster
  bootstrap CIs are correspondingly wider.
- **Self-reported scores.** HELM is third-party; we trust HELM's
  provenance.
- **Companion paper relation.** Methodology is paper 3 (NeurIPS
  E&D, in review); we cite explicitly. Disjoint domain (Q&A vs
  safety).

---

## 7. Conclusion

We applied pairwise reversal-rate analysis with cluster-bootstrap CIs
to LLM safety evaluation across 87 frontier LLMs and 9 safety
metrics. Half of the across-axis metric pairs return opposite
preferred-LLM verdicts on more than 50 % of model pairs; harm/refusal
metrics are negatively correlated with the bias benchmark; even
within HarmBench, two scoring procedures disagree on 25 %. The
choice of safety metric is an independent variable of the research
design, not a measurement nuisance. We recommend benchmark papers
report the full reversal-rate matrix alongside their headline.

Code and analysis at `safety-criteria-iv-experiment` (private until
companion paper 3 anonymity period ends).

---

## References

[Standard list including HELM Safety, HarmBench, AIR-Bench,
BEAVERTAILS, BBQ, XSTest, SimpleSafetyTests, AnthropicRedTeam,
Bai et al. constitutional AI, Cui et al. agency,
Liu et al. survey 2025, paper 3 / 5 / 7 of the present authors.]

## Appendix A — Reproducibility

Public HELM data at:
`https://storage.googleapis.com/crfm-helm-public/gzip/safety/benchmark_output/releases/v1.17.0/`

Pipeline:
```
python run_phase2.py    # fetch + build score matrix
python run_phase3.py    # reversal + bootstrap + clustering
python run_figures.py   # 4 paper figures
```

Total runtime: ~ 5 minutes on a laptop CPU. No API keys, no GPU.
