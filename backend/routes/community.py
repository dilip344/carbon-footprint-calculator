from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ai.forecasting_model import forecast_emissions
from database import get_db
from models.carbon import CarbonRecord
from models.fusion import FusionRecord
from models.user import User
from schemas.community import CommunityInput
from services.community_calculator import calculate_community_breakdown
from services.fusion_pipeline import finalize_fusion, run_fusion
from services.recommendations import generate_recommendations
from services.scoring import sustainability_score

router = APIRouter(prefix="/api/community", tags=["Community"])


def get_user(uid: int, db: Session):
    user = db.query(User).filter(User.id == uid).first()
    if not user:
        raise HTTPException(404, "User not found")
    return user


def _data_from_record(record):
    return {
        "entity_name": record.entity_name,
        "population": record.population or 1,
        "travel_mode": record.travel_mode or "bus",
        "travel_km": record.travel_km or 0,
        "fuel_liters": record.fuel_liters or 0,
        "electricity_kwh": record.electricity_kwh or 0,
        "lpg_kg": record.lpg_kg or 0,
        "water_liters": record.water_liters or 0,
        "waste_kg": record.waste_kg or 0,
        "food_type": record.food_type or "mixed",
        "flights": record.flights or 0,
        "paper_kg": record.paper_kg or 0,
        "trees": record.trees or 0,
    }


def _normalized(data):
    population = max(data["population"], 1)
    result = dict(data)
    for key in ("travel_km", "fuel_liters", "electricity_kwh", "lpg_kg", "water_liters", "waste_kg", "flights", "paper_kg"):
        result[key] = data[key] / population
    result["trees"] = int(data["trees"] / population)
    result.pop("entity_name", None)
    result.pop("population", None)
    return result


def _fusion_dict(fusion):
    if not fusion:
        return None
    return {
        "fused_estimate": fusion.fused_value,
        "deterministic_estimate": fusion.deterministic_value,
        "ml_estimate": fusion.ml_value,
        "confidence_weight": fusion.confidence_weight,
        "s1_distance": fusion.s1_distance,
        "s2_density": fusion.s2_density,
        "s3_residual": fusion.s3_residual,
        "dynamic_threshold": fusion.dynamic_threshold,
        "divergence_flag": bool(fusion.divergence_flag),
        "cluster_id": fusion.cluster_id,
        "fusion_record_id": fusion.id,
    }


def response_for_record(record, db):
    data = _data_from_record(record)
    breakdown = calculate_community_breakdown(data)
    per_person = record.monthly_emissions / max(record.population or 1, 1)
    fusion = db.query(FusionRecord).filter(FusionRecord.carbon_record_id == record.id).first()
    return {
        "id": record.id,
        "mode": "community",
        "entity_name": record.entity_name,
        "population": record.population,
        "user_name": record.user_name,
        "monthly_emissions": record.monthly_emissions,
        "annual_emissions": record.annual_emissions,
        "per_person_monthly": round(per_person, 2),
        "per_person_annual": round(per_person * 12, 2),
        "sustainability_score": record.sustainability_score,
        "cluster": record.cluster,
        "breakdown": breakdown,
        "recommendations": generate_recommendations(data, breakdown),
        "prediction": record.annual_emissions,
        "forecast": forecast_emissions(record.monthly_emissions),
        "peer_average": 1800.0 * max(record.population or 1, 1),
        "fusion": _fusion_dict(fusion),
    }


def community_report_data(record):
    data = _data_from_record(record)
    return data, calculate_community_breakdown(data)


@router.post("/calculate/{uid}")
def calculate(uid: int, data: CommunityInput, db: Session = Depends(get_db)):
    user = get_user(uid, db)
    payload = data.model_dump()
    breakdown = calculate_community_breakdown(payload)
    population = max(payload["population"], 1)
    deterministic_annual_per_person = (breakdown["Total"] * 12.0) / population
    normalized = _normalized(payload)

    try:
        fusion = run_fusion(db, user.id, normalized, deterministic_annual_per_person)
        annual = fusion["fused_annual"] * population
        monthly = annual / 12.0
        record = CarbonRecord(
            user_id=user.id,
            user_name=user.name,
            mode="community",
            entity_name=payload["entity_name"],
            population=population,
            travel_mode=payload["travel_mode"],
            travel_km=payload["travel_km"],
            fuel_liters=payload["fuel_liters"],
            electricity_kwh=payload["electricity_kwh"],
            lpg_kg=payload["lpg_kg"],
            water_liters=payload["water_liters"],
            waste_kg=payload["waste_kg"],
            food_type=payload["food_type"],
            flights=payload["flights"],
            paper_kg=payload["paper_kg"],
            trees=payload["trees"],
            monthly_emissions=monthly,
            annual_emissions=annual,
            sustainability_score=sustainability_score(monthly / population, payload["trees"], normalized),
            cluster=fusion["cluster"],
        )
        db.add(record)
        db.flush()
        finalize_fusion(db, fusion["fusion_record"], record.id, fusion["cluster_id"])
        db.refresh(record)
    except Exception:
        db.rollback()
        raise

    response = response_for_record(record, db)
    return response
