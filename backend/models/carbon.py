from datetime import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from database import Base

class CarbonRecord(Base):
    __tablename__ = "carbon_records"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user_name = Column(String(120), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Dual-mode metadata
    mode = Column(String(20), default="individual", nullable=False)
    entity_name = Column(String(160), nullable=True)
    population = Column(Integer, default=1, nullable=False)

    travel_mode = Column(String(30))
    travel_km = Column(Float)
    fuel_liters = Column(Float)
    electricity_kwh = Column(Float)
    lpg_kg = Column(Float)
    water_liters = Column(Float)
    waste_kg = Column(Float)
    food_type = Column(String(30))
    flights = Column(Float)
    paper_kg = Column(Float)
    trees = Column(Integer)

    monthly_emissions = Column(Float)
    annual_emissions = Column(Float)
    sustainability_score = Column(Float)
    cluster = Column(String(100))
