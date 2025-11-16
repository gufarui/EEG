from __future__ import annotations

import numpy as np
from mne.stats import permutation_cluster_test


def cluster_compare(X: np.ndarray, Y: np.ndarray, n_permutations: int = 1000):
    """Two-condition cluster-based permutation test.

    Parameters
    ----------
    X, Y : arrays of shape (n_subjects, n_times)
    """
    T_obs, clusters, p_vals, h0 = permutation_cluster_test([X, Y], n_permutations=n_permutations, tail=0, n_jobs=1)
    return T_obs, clusters, p_vals, h0

