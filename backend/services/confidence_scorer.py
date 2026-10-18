import math
import numpy as np


def compute_s1_distance(feature_vector, training_mean, training_std):
    """Average absolute z-score: higher means the input is less familiar to the model."""
    values = np.asarray(feature_vector, dtype=float).reshape(-1)
    mean = np.asarray(training_mean, dtype=float)
    std = np.asarray(training_std, dtype=float)
    z = np.abs((values - mean) / (std + 1e-6))
    return float(np.mean(z))


def compute_s2_density(cluster_id, cluster_counts):
    """Normalize the assigned cluster's historical count to the busiest cluster."""
    count = int(cluster_counts.get(cluster_id, 0))
    max_count = max(cluster_counts.values()) if cluster_counts else 1
    return float(count / max_count) if max_count > 0 else 0.0


def compute_confidence_weight(s1, s2, s3, a1=1.0, a2=1.0, a3=1.0):
    """Return w in [0, 1], where larger w means more trust in the Random Forest."""
    raw_score = (a1 / (1.0 + s1)) + (a2 * s2) + (a3 / (1.0 + s3))
    # Center the sigmoid so typical scores sit in a useful middle/high range.
    raw = max(min(raw_score - 1.5, 60.0), -60.0)
    return float(1.0 / (1.0 + math.exp(-raw)))
