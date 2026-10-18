def generate_recommendations(d,b):
 vals={k:v for k,v in b.items() if k not in ("Total","Tree offset") and v>0}; ranked=sorted(vals.items(),key=lambda x:x[1],reverse=True); tips=[]
 if ranked: tips.append(f"Your largest estimated source is {ranked[0][0]}. Start there for the biggest potential reduction.")
 if d["travel_mode"]=="car" and d["fuel_liters"]>30: tips.append("Reduce avoidable car trips, use public transport/carpooling and maintain tyre pressure.")
 if d["electricity_kwh"]>200: tips.append("Use LEDs, efficient appliances and switch off idle equipment.")
 if d["waste_kg"]>15: tips.append("Separate wet/dry waste and compost organic waste where possible.")
 if d["food_type"]=="non_vegetarian": tips.append("Add more plant-based meals each week.")
 if d["flights"]>1: tips.append("Prefer rail or virtual meetings for short trips and avoid unnecessary flights.")
 if d["paper_kg"]>5: tips.append("Use digital documents and print double-sided when necessary.")
 if d["trees"]==0: tips.append("Participate in tree-plantation activities while prioritizing direct emission reductions.")
 return tips[:6] or ["Keep tracking monthly and focus on your largest emission category."]
