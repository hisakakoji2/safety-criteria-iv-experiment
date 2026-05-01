"""Generate paper figures from Phase 3 result JSON.

Outputs:
  figures/fig1_reversal_heatmap.{pdf,png}
  figures/fig2_spearman_dendrogram.{pdf,png}
  figures/fig3_headline_pairs.{pdf,png}
  figures/fig4_ci_overlay.{pdf,png}
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import dendrogram

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
FIGURES.mkdir(exist_ok=True)


SHORT_LABELS = {
    "HarmBench::LM Evaluated Safety score": "HB-LM",
    "HarmBench::Llama Annotator Success Rate": "HB-Llama",
    "HarmBench::GPT Annotator Success Rate": "HB-GPT",
    "SimpleSafetyTests::LM Evaluated Safety score": "SimpleST",
    "XSTest::LM Evaluated Safety score": "XSTest",
    "BBQ::BBQ accuracy": "BBQ-acc",
    "BBQ::BBQ (ambiguous)": "BBQ-amb",
    "BBQ::BBQ (unambiguous)": "BBQ-unamb",
    "AnthropicRedTeam::LM Evaluated Safety score": "AnthrRT",
}


def short(label: str) -> str:
    return SHORT_LABELS.get(label, label[:18])


def _heatmap(ax, df, title, cmap, vmin, vmax, fmt=".2f"):
    im = ax.imshow(df.values, cmap=cmap, vmin=vmin, vmax=vmax, aspect="auto")
    labels = [short(c) for c in df.columns]
    ax.set_xticks(range(len(df.columns)))
    ax.set_yticks(range(len(df.index)))
    ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=9)
    ax.set_yticklabels(labels, fontsize=9)
    for i in range(len(df.index)):
        for j in range(len(df.columns)):
            v = df.values[i, j]
            if np.isnan(v):
                ax.text(j, i, "—", ha="center", va="center",
                        color="grey", fontsize=8)
                continue
            colour = "white" if (vmax > 0.5 and v > 0.45) else "black"
            ax.text(j, i, format(v, fmt), ha="center", va="center",
                    color=colour, fontsize=8)
    ax.set_title(title)
    return im


def fig_reversal_heatmap():
    df = pd.read_csv(RESULTS / "reversal_point.csv", index_col=0)
    df = df.loc[df.columns]
    fig, ax = plt.subplots(figsize=(9, 7.5))
    im = _heatmap(ax, df,
                  "Pairwise reversal rate (87 LLMs × 9 safety metrics)",
                  cmap="Reds", vmin=0.0, vmax=0.7)
    plt.colorbar(im, ax=ax, label="reversal rate")
    plt.tight_layout()
    plt.savefig(FIGURES / "fig1_reversal_heatmap.pdf", bbox_inches="tight")
    plt.savefig(FIGURES / "fig1_reversal_heatmap.png", dpi=200, bbox_inches="tight")
    plt.close()
    print("[fig1] saved")


def fig_spearman_dendrogram():
    rho = pd.read_csv(RESULTS / "spearman.csv", index_col=0)
    rho = rho.loc[rho.columns]
    clust = json.loads((RESULTS / "clustering.json").read_text())
    Z = np.array(clust["linkage"])

    fig = plt.figure(figsize=(13, 7.5))
    gs = fig.add_gridspec(1, 2, width_ratios=[2.2, 1.0], wspace=0.35)
    ax_h = fig.add_subplot(gs[0, 0])
    ax_d = fig.add_subplot(gs[0, 1])

    im = _heatmap(ax_h, rho, "Spearman ρ between safety metrics",
                  cmap="RdBu_r", vmin=-1.0, vmax=1.0)
    plt.colorbar(im, ax=ax_h, label="Spearman ρ")
    short_lbls = [short(c) for c in clust["criteria"]]
    dendrogram(Z, labels=short_lbls, ax=ax_d, leaf_rotation=45)
    ax_d.set_title("Metric clustering (1 − ρ)")
    ax_d.set_ylabel("distance")
    plt.tight_layout()
    plt.savefig(FIGURES / "fig2_spearman_dendrogram.pdf", bbox_inches="tight")
    plt.savefig(FIGURES / "fig2_spearman_dendrogram.png", dpi=200, bbox_inches="tight")
    plt.close()
    print("[fig2] saved")


def fig_headline_pairs():
    summary = json.loads((RESULTS / "phase3_summary.json").read_text())
    head = [h for h in summary["headline_pairs"]
            if not (np.isnan(h["reversal"]) or np.isnan(h["ci_low"]))][:10]

    pairs = []
    for h in head:
        a, b = h["pair"].split(" vs ")
        pairs.append(f"{short(a)}  ↔  {short(b)}")
    rates = [h["reversal"] for h in head]
    los = [h["ci_low"] for h in head]
    his = [h["ci_high"] for h in head]
    rhos = [h["spearman"] for h in head]

    y = np.arange(len(pairs))
    fig, ax = plt.subplots(figsize=(11, 5.8))
    ax.barh(y, rates, color="tab:red", alpha=0.85, height=0.6,
            label="reversal rate")
    err_low = np.array(rates) - np.array(los)
    err_high = np.array(his) - np.array(rates)
    ax.errorbar(rates, y, xerr=[err_low, err_high], fmt="none",
                ecolor="black", capsize=3, linewidth=1)
    for i, r in enumerate(rhos):
        if np.isnan(r):
            continue
        ax.text(rates[i] + 0.005, y[i], f"ρ={r:+.2f}",
                va="center", fontsize=9, color="tab:gray")
    ax.set_yticks(y)
    ax.set_yticklabels(pairs)
    ax.set_xlabel("Pairwise reversal rate (with 95% CI; ρ = avg Spearman)")
    ax.set_title("Top 10 disagreeing safety-metric pairs (87 LLMs)")
    ax.set_xlim(0, max(his) * 1.15)
    ax.invert_yaxis()
    ax.grid(axis="x", alpha=0.3)
    ax.axvline(0.5, color="grey", linestyle=":", linewidth=1)
    plt.tight_layout()
    plt.savefig(FIGURES / "fig3_headline_pairs.pdf", bbox_inches="tight")
    plt.savefig(FIGURES / "fig3_headline_pairs.png", dpi=200, bbox_inches="tight")
    plt.close()
    print("[fig3] saved")


def fig_ci_overlay():
    point = pd.read_csv(RESULTS / "reversal_point.csv", index_col=0)
    low = pd.read_csv(RESULTS / "reversal_ci_low.csv", index_col=0)
    high = pd.read_csv(RESULTS / "reversal_ci_high.csv", index_col=0)
    width = high - low

    fig, axes = plt.subplots(1, 2, figsize=(15, 7))
    im0 = _heatmap(axes[0], width.fillna(0),
                   "95% CI width (high − low)",
                   cmap="Blues", vmin=0.0, vmax=0.20)
    plt.colorbar(im0, ax=axes[0])
    im1 = _heatmap(axes[1], low.fillna(0),
                   "95% CI lower bound",
                   cmap="Reds", vmin=0.0, vmax=0.7)
    plt.colorbar(im1, ax=axes[1])
    plt.tight_layout()
    plt.savefig(FIGURES / "fig4_ci_overlay.pdf", bbox_inches="tight")
    plt.savefig(FIGURES / "fig4_ci_overlay.png", dpi=200, bbox_inches="tight")
    plt.close()
    print("[fig4] saved")


def main():
    fig_reversal_heatmap()
    fig_spearman_dendrogram()
    fig_headline_pairs()
    fig_ci_overlay()
    print(f"[figures] all saved to {FIGURES}/")


if __name__ == "__main__":
    main()
