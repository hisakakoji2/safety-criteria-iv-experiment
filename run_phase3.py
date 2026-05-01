"""Phase 3 — Reversal rate + bootstrap CI + clustering on the HELM Safety
score matrix.
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

import pandas as pd

from src.analysis import (
    all_pairwise_reversals, all_rank_correlations, bootstrap_reversal,
)
from src.clustering import cluster_criteria


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="results/score_matrix_helm.csv")
    ap.add_argument("--bootstrap", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=20260501)
    args = ap.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    log = logging.getLogger("phase3")

    df = pd.read_csv(args.input, index_col=0)
    log.info("[load] %d models × %d metrics", *df.shape)

    log.info("[reversal] point estimates")
    rev_point = all_pairwise_reversals(df)
    rev_point.to_csv(RESULTS / "reversal_point.csv")
    log.info("\n%s", rev_point.round(3).to_string())

    log.info("[spearman]")
    rho = all_rank_correlations(df, kind="spearman")
    rho.to_csv(RESULTS / "spearman.csv")
    log.info("\n%s", rho.round(3).to_string())

    log.info("[bootstrap] B=%d, cluster bootstrap over models", args.bootstrap)
    _, ci_low, ci_high = bootstrap_reversal(df, n_samples=args.bootstrap, seed=args.seed)
    ci_low.to_csv(RESULTS / "reversal_ci_low.csv")
    ci_high.to_csv(RESULTS / "reversal_ci_high.csv")

    log.info("[cluster] hierarchical clustering")
    clust = cluster_criteria(rho, n_clusters=min(3, len(rho.columns) - 1))
    Path(RESULTS / "clustering.json").write_text(json.dumps(clust, indent=2))
    log.info("  cluster labels: %s", dict(zip(clust["criteria"], clust["labels"])))

    # Headline pairs: top 10 by reversal point estimate
    crits = list(rev_point.columns)
    headline = []
    for i, ci in enumerate(crits):
        for j, cj in enumerate(crits):
            if j <= i:
                continue
            headline.append({
                "pair": f"{ci} vs {cj}",
                "reversal": float(rev_point.loc[ci, cj]),
                "ci_low": float(ci_low.loc[ci, cj]),
                "ci_high": float(ci_high.loc[ci, cj]),
                "spearman": float(rho.loc[ci, cj]),
            })
    headline.sort(key=lambda x: -x["reversal"])
    log.info("[headline] top 10 pairs by reversal:")
    for h in headline[:10]:
        log.info("  %.4f  CI=[%.4f, %.4f]  rho=%+.3f  %s",
                 h["reversal"], h["ci_low"], h["ci_high"],
                 h["spearman"], h["pair"])

    summary = {
        "n_models": int(len(df)),
        "n_metrics": int(len(crits)),
        "metric_names": crits,
        "reversal_point": rev_point.to_dict(),
        "reversal_ci_low": ci_low.to_dict(),
        "reversal_ci_high": ci_high.to_dict(),
        "spearman": rho.to_dict(),
        "clustering": clust,
        "headline_pairs": headline,
    }
    Path(RESULTS / "phase3_summary.json").write_text(
        json.dumps(summary, indent=2, default=str)
    )
    log.info("[done] saved to %s", RESULTS)


if __name__ == "__main__":
    main()
