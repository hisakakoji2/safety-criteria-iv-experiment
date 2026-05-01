"""HELM Safety v1.17.0 score loader.

Fetches per-benchmark JSON tables from the HELM public bucket,
extracts (model, metric) → score mappings, and consolidates into a
single (n_models × n_metrics) DataFrame.

Source release:
  https://storage.googleapis.com/crfm-helm-public/gzip/safety/
  benchmark_output/releases/v1.17.0/

Each per-group JSON is a list with one section; the section has a
header (column names) and rows (per-model data). The first column is
the model name (with link metadata); subsequent columns are metrics.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from urllib.request import urlretrieve

import pandas as pd


HELM_RELEASE = "v1.17.0"
HELM_BASE = (
    "https://storage.googleapis.com/crfm-helm-public/gzip/safety/"
    f"benchmark_output/releases/{HELM_RELEASE}"
)


# (group_id, friendly_name, list of metric column names to extract)
HELM_GROUPS = [
    # group_id              friendly         metric_column_substrings
    ("harm_bench",          "HarmBench",     ["Llama Annotator", "GPT Annotator", "Safety score"]),
    ("simple_safety_tests", "SimpleSafetyTests", ["LM Evaluated"]),
    ("xstest",              "XSTest",        ["LM Evaluated"]),
    ("bbq",                 "BBQ",           ["BBQ", "EM"]),
    ("anthropic_red_team",  "AnthropicRedTeam", ["LM Evaluated"]),
]


log = logging.getLogger(__name__)


@dataclass
class HelmScores:
    df: pd.DataFrame  # index: model name, columns: metric names
    raw_groups: dict[str, list]


def fetch_group_json(group_id: str, cache_dir: Path) -> list:
    cache_dir.mkdir(parents=True, exist_ok=True)
    target = cache_dir / f"{group_id}.json"
    if not target.exists():
        url = f"{HELM_BASE}/groups/{group_id}.json"
        log.info("[fetch] %s", url)
        urlretrieve(url, target)
    return json.loads(target.read_text())


def _extract_value(cell):
    """HELM cells are dicts with 'value' (number or string)."""
    if isinstance(cell, dict):
        return cell.get("value")
    return cell


def parse_group(
    group_data: list, group_friendly: str, metric_keywords: list[str],
) -> dict[tuple[str, str], float]:
    """Parse one group JSON into {(model, metric_label): score} mapping."""
    out: dict[tuple[str, str], float] = {}
    if not group_data or not isinstance(group_data, list):
        return out
    for section in group_data:
        header = section.get("header", [])
        col_names = [_extract_value(h) for h in header]
        for row in section.get("rows", []):
            if not row:
                continue
            model_name = _extract_value(row[0])
            if not model_name:
                continue
            for ci, col_name in enumerate(col_names[1:], start=1):
                if ci >= len(row):
                    continue
                col_str = str(col_name)
                if not any(kw.lower() in col_str.lower() for kw in metric_keywords):
                    continue
                val = _extract_value(row[ci])
                if isinstance(val, (int, float)):
                    metric_label = f"{group_friendly}::{col_str}"
                    out[(str(model_name), metric_label)] = float(val)
    return out


def load_helm_safety_scores(cache_dir: str | Path = "data/helm_safety") -> HelmScores:
    cache_dir = Path(cache_dir) / "groups"
    raw_groups: dict[str, list] = {}
    all_scores: dict[tuple[str, str], float] = {}
    for group_id, friendly, kws in HELM_GROUPS:
        try:
            g = fetch_group_json(group_id, cache_dir)
            raw_groups[group_id] = g
            scores = parse_group(g, friendly, kws)
            log.info("  [%s] %d (model, metric) pairs extracted",
                     friendly, len(scores))
            all_scores.update(scores)
        except Exception as e:
            log.warning("  [%s] failed: %s", group_id, e)
            continue

    # Build wide DataFrame
    rows: dict[str, dict[str, float]] = {}
    for (model, metric), v in all_scores.items():
        rows.setdefault(model, {})[metric] = v
    df = pd.DataFrame.from_dict(rows, orient="index")
    df = df.sort_index()
    log.info("[HELM] consolidated: %d models × %d metrics", *df.shape)
    return HelmScores(df=df, raw_groups=raw_groups)
