from typing import Literal
from pydantic import BaseModel,Field
class CarbonInput(BaseModel):
 travel_mode:Literal["bike","car","bus","train","walk","other"]="car"
 travel_km:float=Field(0,ge=0); fuel_liters:float=Field(0,ge=0); electricity_kwh:float=Field(0,ge=0); lpg_kg:float=Field(0,ge=0); water_liters:float=Field(0,ge=0); waste_kg:float=Field(0,ge=0); food_type:Literal["vegetarian","mixed","non_vegetarian"]="mixed"; flights:float=Field(0,ge=0); paper_kg:float=Field(0,ge=0); trees:int=Field(0,ge=0)
