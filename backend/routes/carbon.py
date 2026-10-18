from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from ai.forecasting_model import forecast_emissions
from database import get_db
from models.carbon import CarbonRecord
from models.fusion import FusionRecord
from models.user import User
from schemas.carbon import CarbonInput
from services.carbon_calculator import calculate_breakdown
from services.fusion_pipeline import finalize_fusion, run_fusion
from services.recommendations import generate_recommendations
from services.report import build_report
from services.scoring import sustainability_score

router = APIRouter(prefix="/api/carbon", tags=["Carbon"])


def get_user(uid: int, db: Session):
    user = db.query(User).filter(User.id == uid).first()
    if not user:
        raise HTTPException(404, "User not found")
    return user


def _input_from_record(record):
    return {
        "travel_mode": record.travel_mode or "car",
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


def _response(record, data, db):
    breakdown = calculate_breakdown(data)
    fusion = (
        db.query(FusionRecord)
        .filter(FusionRecord.carbon_record_id == record.id)
        .first()
    )
    return {
        "id": record.id,
        "mode": record.mode,
        "user_name": record.user_name,
        "monthly_emissions": record.monthly_emissions,
        "annual_emissions": record.annual_emissions,
        "sustainability_score": record.sustainability_score,
        "cluster": record.cluster,
        "breakdown": breakdown,
        "recommendations": generate_recommendations(data, breakdown),
        "prediction": record.annual_emissions,
        "forecast": forecast_emissions(record.monthly_emissions),
        "peer_average": 1800.0,
        "fusion": _fusion_dict(fusion),
    }


@router.post("/calculate/{uid}")
def calculate(uid: int, data: CarbonInput, db: Session = Depends(get_db)):
    user = get_user(uid, db)
    payload = data.model_dump()
    breakdown = calculate_breakdown(payload)
    deterministic_annual = breakdown["Total"] * 12.0

    try:
        fusion = run_fusion(db, user.id, payload, deterministic_annual)
        monthly = fusion["fused_monthly"]
        annual = fusion["fused_annual"]
        record = CarbonRecord(
            user_id=user.id,
            user_name=user.name,
            mode="individual",
            entity_name=None,
            population=1,
            **payload,
            monthly_emissions=monthly,
            annual_emissions=annual,
            sustainability_score=sustainability_score(monthly, payload["trees"], payload),
            cluster=fusion["cluster"],
        )
        db.add(record)
        db.flush()
        finalize_fusion(db, fusion["fusion_record"], record.id, fusion["cluster_id"])
        db.refresh(record)
    except Exception:
        db.rollback()
        raise

    return _response(record, payload, db)


@router.get("/latest/{uid}")
def latest(uid: int, mode: str = Query("individual", pattern="^(individual|community)$"), db: Session = Depends(get_db)):
    get_user(uid, db)
    record = (
        db.query(CarbonRecord)
        .filter(CarbonRecord.user_id == uid, CarbonRecord.mode == mode)
        .order_by(CarbonRecord.created_at.desc())
        .first()
    )
    if not record:
        return {"record": None}

    if mode == "community":
        from routes.community import response_for_record
        return response_for_record(record, db)
    return _response(record, _input_from_record(record), db)


@router.get("/history/{uid}")
def history(uid: int, mode: str = Query("individual", pattern="^(individual|community)$"), db: Session = Depends(get_db)):
    get_user(uid, db)
    rows = (
        db.query(CarbonRecord)
        .filter(CarbonRecord.user_id == uid, CarbonRecord.mode == mode)
        .order_by(CarbonRecord.created_at.desc())
        .limit(50)
        .all()
    )
    return [
        {
            "id": r.id,
            "date": r.created_at.strftime("%Y-%m-%d %H:%M"),
            "mode": r.mode,
            "entity_name": r.entity_name,
            "population": r.population,
            "monthly_emissions": r.monthly_emissions,
            "annual_emissions": r.annual_emissions,
            "score": r.sustainability_score,
            "cluster": r.cluster,
        }
        for r in rows
    ]


@router.get("/fusion/{uid}")
def fusion_history(uid: int, mode: str = Query("individual", pattern="^(individual|community)$"), db: Session = Depends(get_db)):
    get_user(uid, db)
    rows = (
        db.query(FusionRecord)
        .join(CarbonRecord, FusionRecord.carbon_record_id == CarbonRecord.id)
        .filter(FusionRecord.user_id == uid, CarbonRecord.mode == mode)
        .order_by(FusionRecord.created_at.desc())
        .limit(50)
        .all()
    )
    return [
        {
            "id": r.id,
            "record_id": r.carbon_record_id,
            "cluster_id": r.cluster_id,
            "deterministic": r.deterministic_value,
            "ml": r.ml_value,
            "fused": r.fused_value,
            "confidence": r.confidence_weight,
            "s1": r.s1_distance,
            "s2": r.s2_density,
            "s3": r.s3_residual,
            "divergence": bool(r.divergence_flag),
            "threshold": r.dynamic_threshold,
            "date": r.created_at.strftime("%Y-%m-%d %H:%M"),
        }
        for r in rows
    ]


@router.get("/report/{rid}")
def report(rid: int, db: Session = Depends(get_db)):
    record = db.query(CarbonRecord).filter(CarbonRecord.id == rid).first()
    if not record:
        raise HTTPException(404, "Report not found")

    if record.mode == "community":
        from routes.community import community_report_data
        data, breakdown = community_report_data(record)
    else:
        data = _input_from_record(record)
        breakdown = calculate_breakdown(data)

    recommendations = generate_recommendations(data, breakdown)
    forecast = forecast_emissions(record.monthly_emissions)
    fusion = db.query(FusionRecord).filter(FusionRecord.carbon_record_id == record.id).first()
    fusion_details = _fusion_dict(fusion)
    pdf = build_report(
        record,
        breakdown,
        recommendations,
        record.annual_emissions,
        forecast,
        fusion_details,
    )
    filename = f'greenpulse-{"community" if record.mode == "community" else "individual"}-report-{rid}.pdf'
    return StreamingResponse(
        pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
