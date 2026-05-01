# safety-criteria-iv-experiment

**The Safety Metric is the Independent Variable: Pairwise Reversal
Rates Reveal What Aggregate Scores Hide in LLM Safety Evaluation**

Status: Phase 1 (design + prior work) complete. Phase 2 (leaderboard
scraping + score matrix) next. Repository private. Held for TMLR
submission until companion-paper anonymity periods end.

## What this is

The fourth cross-domain validation of the criterion-as-independent-
variable framework, applied to **LLM safety evaluation**. Where the
field treats "safety SOTA" as a single quantity, we treat the choice
of safety benchmark as a research-design variable and quantify the
case-level disagreement rate across benchmark pairs.

## Headline question

> When 8-12 frontier LLMs are scored on each of 8-10 public safety
> benchmarks (HELM Safety, AIR-Bench, HarmBench, AdvBench, SORRY-Bench,
> AlpacaEval, WildBench, TruthfulQA, BBQ, ToxiGen), how often does the
> pairwise LLM ranking flip between benchmarks?

## Pre-registered hypotheses

- **H1** ≥ 1 pair has reversal rate ≥ 30 %, CI lower bound > 25 %
- **H2** ≥ 1 pair has Spearman ρ ≥ 0.50 *and* reversal ≥ 25 %
- **H3** Hierarchical clustering separates helpfulness vs harmlessness
- **H4** Within-axis pairs have median reversal < across-axis pairs
- **H5** Pattern matches paper 3 (LLM Q&A) and paper 7 (T2I)

## Layout

```
safety-criteria-iv-experiment/
├── README.md
├── meta/
│   ├── prior_work.md            literature map (HELM, AIR-Bench,
│                                  HarmBench, BEAVERTAILS, ...)
│   └── experiment_design.md     pre-registered protocol + H1-H5
├── src/                         (planned) score collectors + analysis
├── tests/                       (planned)
├── data/                        (planned) leaderboard scrapings
├── results/                     (planned) reversal/Spearman matrices
├── figures/                     (planned) 4 paper figures
├── paper/                       (planned) main.md + LaTeX
└── docs/
```

## Methodology source

This paper is the fourth cross-domain validation of the criterion-as-IV
framework:

| Paper | Domain | Status |
|---|---|---|
| paper 3: criteria-iv-experiment | LLM Q&A | NeurIPS E&D submission |
| paper 5: finance-criteria-iv-experiment | Fund ranking | companion submission |
| paper 7: image-criteria-iv-experiment | T2I evaluation | companion submission |
| **this paper** | **LLM safety** | **draft (Phase 1)** |

## Submission

- **Primary venue**: TMLR (rolling, long-format)
- **Backup**: NeurIPS 2026 Workshop on Trustworthy ML
- **Submission timing**: after paper 3 (NeurIPS E&D) author
  notification, 2026-09-24

## License

MIT.
