from datetime import datetime
from sqlalchemy.orm import Session
from models.fusion import FusionRecord, ClusterResidualStats


def get_cluster_counts(db: Session):
    rows = db.query(FusionRecord.cluster_id).all()
    counts = {}
    for (cluster_id,) in rows:
        counts[cluster_id] = counts.get(cluster_id, 0) + 1
    return counts


def get_cluster_residual_dict(db: Session):
    rows = db.query(ClusterResidualStats).all()
    return {row.cluster_id: float(row.mean_abs_error or 0.0) for row in rows}


def update_cluster_residuals(db: Session, cluster_id: int):
    """Recompute mean |D-M| for one cluster after a calculation is stored."""
    records = db.query(FusionRecord).filter(FusionRecord.cluster_id == cluster_id).all()
    if not records:
        return

    errors = [abs((r.deterministic_value or 0.0) - (r.ml_value or 0.0)) for r in records]
    mean_error = sum(errors) / len(errors)
    stats = db.query(ClusterResidualStats).filter_by(cluster_id=cluster_id).first()

    if stats:
        stats.mean_abs_error = mean_error
        stats.sample_count = len(records)
        stats.updated_at = datetime.utcnow()
    else:
        db.add(
            ClusterResidualStats(
                cluster_id=cluster_id,
                mean_abs_error=mean_error,
                sample_count=len(records),
            )
        )
    db.commit()
