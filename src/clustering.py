"""Hierarchical clustering of metrics by 1 - Spearman ρ. Ported from
image-criteria-iv-experiment / finance-criteria-iv-experiment.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import squareform


def cluster_criteria(rho_matrix: pd.DataFrame, n_clusters: int = 3) -> dict:
    distance = 1.0 - rho_matrix.fillna(0.0).to_numpy()
    np.fill_diagonal(distance, 0.0)
    distance = (distance + distance.T) / 2.0
    np.fill_diagonal(distance, 0.0)
    condensed = squareform(distance, checks=False)
    Z = linkage(condensed, method="average")
    labels = fcluster(Z, t=n_clusters, criterion="maxclust")
    return {
        "criteria": list(rho_matrix.columns),
        "labels": labels.tolist(),
        "linkage": Z.tolist(),
        "n_clusters": int(n_clusters),
    }
