import json
from pathlib import Path
from sqlalchemy.orm import Session

from ai.clustering_model import cluster_label, predict_cluster_id
from ai.prediction_model import predict_annual
from ai.preprocessing import vector_from_payload
from models.fusion import FusionRecord
from services.fusion_engine import fuse_estimates
from services.recalibration import (
    get_cluster_counts,
    get_cluster_residual_dict,
    update_cluster_residuals,
)

ROOT = Path(__file__).resolve().parents[2]
STATS_PATH = ROOT / "ai" / "training_stats.json"


def _training_stats():
    with STATS_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def run_fusion(
    db: Session,
    user_id: int,
    payload: dict,
    deterministic_annual: float,
):
    """Run D + Random Forest + K-Means + adaptive fusion and persist an audit record."""
    stats = _training_stats()
    feature_vector = vector_from_payload(payload)
    cluster_id = predict_cluster_id(payload)
    ml_annual = predict_annual(payload)

    fusion = fuse_estimates(
        deterministic_value=deterministic_annual,
        ml_value=ml_annual,
        feature_vector=feature_vector,
        cluster_id=cluster_id,
        training_mean=stats["mean"],
        training_std=stats["std"],
        cluster_counts=get_cluster_counts(db),
        cluster_residuals=get_cluster_residual_dict(db),
    )

    record = FusionRecord(
        user_id=user_id,
        cluster_id=cluster_id,
        deterministic_value=float(deterministic_annual),
        ml_value=float(ml_annual),
        fused_value=float(fusion["fused_value"]),
        confidence_weight=float(fusion["weight"]),
        s1_distance=float(fusion["s1"]),
        s2_density=float(fusion["s2"]),
        s3_residual=float(fusion["s3"]),
        divergence_flag=bool(fusion["divergence_flag"]),
        dynamic_threshold=float(fusion["dynamic_threshold"]),
    )
    db.add(record)
    db.flush()

    return {
        **fusion,
        "cluster_id": cluster_id,
        "cluster": cluster_label(cluster_id),
        "deterministic_annual": float(deterministic_annual),
        "ml_annual": float(ml_annual),
        "fused_annual": float(fusion["fused_value"]),
        "fused_monthly": float(fusion["fused_value"] / 12.0),
        "fusion_record": record,
    }


def finalize_fusion(db: Session, fusion_record: FusionRecord, carbon_record_id: int, cluster_id: int):
    """Link the fusion audit row to the final carbon record and refresh residual stats."""
    fusion_record.carbon_record_id = carbon_record_id
    db.flush()
    db.commit()
    db.refresh(fusion_record)
    update_cluster_residuals(db, cluster_id)
