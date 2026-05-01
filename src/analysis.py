"""Pairwise reversal-rate analysis on (model × metric) score matrix.

Adapted from image-criteria-iv-experiment / finance-criteria-iv-experiment:
the *unit of comparison* here is a pair of LLMs (not a within-prompt
image pair), and the reversal asks "given two metrics, do they
disagree on the ordering of LLM_i vs LLM_j?".
"""

from __future__ import annotations

from itertools import combinations

import numpy as np
import pandas as pd
from scipy import stats


def reversal_rate_metric_pair(
    score_a: pd.Series, score_b: pd.Series,
) -> tuple[float, int, int]:
    """For two metrics scored over the same model panel, compute the
    pairwise reversal rate over all model pairs.
    """
    common = score_a.index.intersection(score_b.index)
    a = score_a.loc[common].to_numpy()
    b = score_b.loc[common].to_numpy()
    valid = ~(np.isnan(a) | np.isnan(b))
    a = a[valid]
    b = b[valid]
    n = len(a)
    if n < 2:
        return float("nan"), 0, 0
    n_flips = 0
    n_decided = 0
    for i in range(n):
        for j in range(i + 1, n):
            sign_a = np.sign(a[j] - a[i])
            sign_b = np.sign(b[j] - b[i])
            if sign_a == 0 or sign_b == 0:
                continue
            n_decided += 1
            if sign_a * sign_b == -1:
                n_flips += 1
    if n_decided == 0:
        return float("nan"), 0, 0
    return n_flips / n_decided, n_flips, n_decided


def all_pairwise_reversals(score_df: pd.DataFrame) -> pd.DataFrame:
    """Symmetric N_metrics × N_metrics matrix of pairwise reversal rates."""
    metrics = list(score_df.columns)
    out = pd.DataFrame(0.0, index=metrics, columns=metrics)
    for c1, c2 in combinations(metrics, 2):
        rate, _, _ = reversal_rate_metric_pair(score_df[c1], score_df[c2])
        out.loc[c1, c2] = rate
        out.loc[c2, c1] = rate
    return out


def all_rank_correlations(
    score_df: pd.DataFrame, kind: str = "spearman",
) -> pd.DataFrame:
    metrics = list(score_df.columns)
    out = pd.DataFrame(1.0, index=metrics, columns=metrics)
    for c1, c2 in combinations(metrics, 2):
        a = score_df[c1].dropna()
        b = score_df[c2].dropna()
        common = a.index.intersection(b.index)
        if len(common) < 4:
            v = float("nan")
        elif kind == "spearman":
            v, _ = stats.spearmanr(a.loc[common], b.loc[common])
        elif kind == "kendall":
            v, _ = stats.kendalltau(a.loc[common], b.loc[common])
        else:
            raise ValueError(kind)
        out.loc[c1, c2] = v
        out.loc[c2, c1] = v
    return out


def bootstrap_reversal(
    score_df: pd.DataFrame, n_samples: int = 1000, seed: int = 20260501,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Cluster-bootstrap over LLMs.
    Returns (point, ci_low, ci_high) of the reversal-rate matrix.
    """
    rng = np.random.default_rng(seed)
    metrics = list(score_df.columns)
    n_models = len(score_df)
    point = all_pairwise_reversals(score_df)

    samples = []
    for b in range(n_samples):
        idx = rng.integers(0, n_models, size=n_models)
        sub = score_df.iloc[idx].copy()
        # Re-key to avoid duplicate index issues
        sub.index = [f"{i}_{name}" for i, name in enumerate(sub.index)]
        samples.append(all_pairwise_reversals(sub))
        if (b + 1) % max(1, n_samples // 10) == 0:
            print(f"  bootstrap: {b+1}/{n_samples}", flush=True)

    arr = np.stack([s.to_numpy() for s in samples], axis=0)
    ci_low = pd.DataFrame(
        np.quantile(arr, 0.025, axis=0),
        index=point.index, columns=point.columns,
    )
    ci_high = pd.DataFrame(
        np.quantile(arr, 0.975, axis=0),
        index=point.index, columns=point.columns,
    )
    return point, ci_low, ci_high
