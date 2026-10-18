FEATURES=["travel_km","fuel_liters","electricity_kwh","lpg_kg","water_liters","waste_kg","flights","paper_kg","trees"]
def vector_from_payload(d):return [[float(d.get(x,0)) for x in FEATURES]]
