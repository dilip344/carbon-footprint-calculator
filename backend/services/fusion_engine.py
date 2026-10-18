from services.confidence_scorer import (
    compute_confidence_weight,
    compute_s1_distance,
    compute_s2_density,
)


def fuse_estimates(
    deterministic_value,
    ml_value,
    feature_vector,
    cluster_id,
    training_mean,
    training_std,
    cluster_counts,
    cluster_residuals,
):
    """Adaptive Hybrid Emission Fusion.

    D = deterministic estimate, M = Random Forest estimate.
    w dynamically controls how much M contributes to final F.
    """
    s1 = compute_s1_distance(feature_vector, training_mean, training_std)
    s2 = compute_s2_density(cluster_id, cluster_counts)
    s3 = float(cluster_residuals.get(cluster_id, 0.0))
    w = compute_confidence_weight(s1, s2, s3)

    fused_value = (w * float(ml_value)) + ((1.0 - w) * float(deterministic_value))

    base_threshold = 0.15 * max(float(deterministic_value), 0.0)
    dynamic_threshold = base_threshold * (1.0 + s1)
    divergence = abs(float(deterministic_value) - float(ml_value)) > dynamic_threshold

    return {
        "fused_value": float(max(fused_value, 0.0)),
        "weight": w,
        "s1": float(s1),
        "s2": float(s2),
        "s3": s3,
        "dynamic_threshold": float(dynamic_threshold),
        "divergence_flag": bool(divergence),
    }
