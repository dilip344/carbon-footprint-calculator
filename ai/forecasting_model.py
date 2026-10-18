import numpy as np
from sklearn.linear_model import LinearRegression
def forecast_emissions(current,months=6):
 hist=np.array([current*(1.02**i) for i in range(6,0,-1)]); x=np.arange(1,7).reshape(-1,1); m=LinearRegression().fit(x,hist); vals=m.predict(np.arange(7,7+months).reshape(-1,1)); return [{"month":i+1,"estimated_emissions":round(max(float(v),0),2)} for i,v in enumerate(vals)]
