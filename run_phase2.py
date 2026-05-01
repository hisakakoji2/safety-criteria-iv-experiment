"""Phase 2 — Build the LLM × safety metric score matrix from HELM Safety.

Fetches v1.17.0 release JSONs (already cached in data/helm_safety/) and
consolidates them into a single CSV that the analysis pipeline can
consume.

Future-Phase additions (not in this script):
  * AIR-Bench 2024 separate fetch (different URL structure)
  * AlpacaEval / WildBench / Arena Hard from their own leaderboards
  * SORRY-Bench from GitHub
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

from src.helm_loader import load_helm_safety_scores


ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="results/score_matrix_helm.csv")
    ap.add_argument("--min-coverage", type=float, default=0.7,
                    help="Drop models with fewer than this fraction of metrics covered")
    args = ap.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    log = logging.getLogger("phase2")

    log.info("[load] HELM Safety v1.17.0 scores")
    helm = load_helm_safety_scores()
    df = helm.df

    log.info("[matrix] raw: %d models × %d metrics", *df.shape)
    coverage = df.notna().mean(axis=1)
    keep = coverage >= args.min_coverage
    df_filt = df[keep]
    log.info("[matrix] after coverage filter (>= %.0f%%): %d models × %d metrics",
             args.min_coverage * 100, *df_filt.shape)

    # Save
    df_filt.to_csv(args.out)
    log.info("[done] saved to %s", args.out)

    # Brief summary
    log.info("[metrics] columns:")
    for col in df_filt.columns:
        n = df_filt[col].notna().sum()
        mean = df_filt[col].mean()
        log.info("  %s: n=%d mean=%.4f", col, n, mean)

    # Save raw_groups for traceability
    raw_path = RESULTS / "helm_groups_raw.json"
    raw_path.write_text(json.dumps(
        {gid: data for gid, data in helm.raw_groups.items()},
        indent=2, default=str,
    ))
    log.info("[done] raw HELM JSONs saved to %s", raw_path)


if __name__ == "__main__":
    main()
