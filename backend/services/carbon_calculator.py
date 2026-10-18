FACTORS={"travel":{"car":.192,"bike":.103,"bus":.105,"train":.041,"walk":0,"other":.15},"fuel":2.31,"electricity":.82,"lpg":3.0,"water":.00030,"waste":.45,"food":{"vegetarian":.9,"mixed":1.7,"non_vegetarian":2.8},"flight":250.0,"paper":1.3,"tree_sequestration":21.0}
def calculate_breakdown(d):
 if d["travel_mode"]=="car" and d["fuel_liters"]>0: travel=0; fuel=d["fuel_liters"]*FACTORS["fuel"]
 else: travel=d["travel_km"]*30*FACTORS["travel"][d["travel_mode"]]; fuel=0
 electricity=d["electricity_kwh"]*FACTORS["electricity"]; lpg=d["lpg_kg"]*FACTORS["lpg"]; water=d["water_liters"]*30*FACTORS["water"]; waste=d["waste_kg"]*FACTORS["waste"]; food=FACTORS["food"][d["food_type"]]*30; flights=d["flights"]*FACTORS["flight"]; paper=d["paper_kg"]*FACTORS["paper"]
 gross=travel+fuel+electricity+lpg+water+waste+food+flights+paper; offset=d["trees"]*FACTORS["tree_sequestration"]/12; total=max(gross-offset,0)
 return {"Travel":round(travel,2),"Fuel":round(fuel,2),"Electricity":round(electricity,2),"LPG":round(lpg,2),"Water":round(water,2),"Waste":round(waste,2),"Food":round(food,2),"Air travel":round(flights,2),"Paper":round(paper,2),"Tree offset":round(-offset,2),"Total":round(total,2)}
def calculate_monthly(d):return calculate_breakdown(d)["Total"]
def calculate_annual(d):return calculate_monthly(d)*12
