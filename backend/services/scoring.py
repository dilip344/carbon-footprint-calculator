def sustainability_score(monthly,trees,d):
 score=max(0,100-monthly/8)+min(trees*.5,10)+(5 if d["travel_mode"] in ("bus","train","bike","walk") else 0)+(5 if d["food_type"]=="vegetarian" else 0); return round(min(100,score),1)
