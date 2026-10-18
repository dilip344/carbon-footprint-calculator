from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer
from database import Base


class FusionRecord(Base):
    __tablename__ = "fusion_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    carbon_record_id = Column(Integer, ForeignKey("carbon_records.id"), nullable=True, index=True)
    cluster_id = Column(Integer, index=True)
    deterministic_value = Column(Float)
    ml_value = Column(Float)
    fused_value = Column(Float)
    confidence_weight = Column(Float)
    s1_distance = Column(Float)
    s2_density = Column(Float)
    s3_residual = Column(Float)
    divergence_flag = Column(Boolean, default=False)
    dynamic_threshold = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ClusterResidualStats(Base):
    __tablename__ = "cluster_residual_stats"

    cluster_id = Column(Integer, primary_key=True)
    mean_abs_error = Column(Float, default=0.0)
    sample_count = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow)
