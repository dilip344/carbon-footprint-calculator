FACTORS = {
    "travel": {"car": 0.192, "bike": 0.103, "bus": 0.105, "train": 0.041, "walk": 0.0, "other": 0.15},
    "fuel": 2.31,
    "electricity": 0.82,
    "lpg": 3.0,
    "water": 0.00030,
    "waste": 0.45,
    "food": {"vegetarian": 0.9, "mixed": 1.7, "non_vegetarian": 2.8},
    "flight": 250.0,
    "paper": 1.3,
    "tree_sequestration": 21.0,
}

def calculate_community_breakdown(d):
    # Community inputs are aggregate monthly totals unless stated otherwise.
    if d["travel_mode"] == "car" and d["fuel_liters"] > 0:
        travel = 0
        fuel = d["fuel_liters"] * FACTORS["fuel"]
    else:
        travel = d["travel_km"] * FACTORS["travel"][d["travel_mode"]]
        fuel = 0

    electricity = d["electricity_kwh"] * FACTORS["electricity"]
    lpg = d["lpg_kg"] * FACTORS["lpg"]
    water = d["water_liters"] * FACTORS["water"]
    waste = d["waste_kg"] * FACTORS["waste"]
    food = FACTORS["food"][d["food_type"]] * 30 * d["population"]
    flights = d["flights"] * FACTORS["flight"]
    paper = d["paper_kg"] * FACTORS["paper"]
    offset = d["trees"] * FACTORS["tree_sequestration"] / 12

    gross = travel + fuel + electricity + lpg + water + waste + food + flights + paper
    total = max(gross - offset, 0)

    return {
        "Travel": round(travel, 2),
        "Fuel": round(fuel, 2),
        "Electricity": round(electricity, 2),
        "LPG": round(lpg, 2),
        "Water": round(water, 2),
        "Waste": round(waste, 2),
        "Food": round(food, 2),
        "Air travel": round(flights, 2),
        "Paper": round(paper, 2),
        "Tree offset": round(-offset, 2),
        "Total": round(total, 2),
    }
