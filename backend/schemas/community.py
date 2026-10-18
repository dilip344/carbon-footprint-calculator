from typing import Literal
from pydantic import BaseModel, Field

class CommunityInput(BaseModel):
    entity_name: str = Field(..., min_length=2, max_length=160)
    population: int = Field(..., ge=1, le=1000000)
    travel_mode: Literal["bike","car","bus","train","walk","other"] = "bus"
    travel_km: float = Field(0, ge=0, description="Aggregate travel distance per month in km")
    fuel_liters: float = Field(0, ge=0, description="Aggregate petrol/diesel per month in litres")
    electricity_kwh: float = Field(0, ge=0)
    lpg_kg: float = Field(0, ge=0)
    water_liters: float = Field(0, ge=0, description="Aggregate water use per month in litres")
    waste_kg: float = Field(0, ge=0)
    food_type: Literal["vegetarian","mixed","non_vegetarian"] = "mixed"
    flights: float = Field(0, ge=0, description="Aggregate flights per month")
    paper_kg: float = Field(0, ge=0)
    trees: int = Field(0, ge=0)
