from pathlib import Path
import joblib,pandas as pd
from sklearn.ensemble import RandomForestRegressor
from ai.preprocessing import FEATURES,vector_from_payload
ROOT=Path(__file__).resolve().parent; DATA=ROOT.parent/"datasets"/"carbon_data.csv"; OUT=ROOT/"trained_models"; OUT.mkdir(exist_ok=True); PATH=OUT/"prediction.joblib"
def train():
 df=pd.read_csv(DATA); m=RandomForestRegressor(n_estimators=180,max_depth=12,random_state=42); m.fit(df[FEATURES],df.annual_emissions); joblib.dump(m,PATH); return m
def get_model():return joblib.load(PATH) if PATH.exists() else train()
def predict_annual(d):return float(get_model().predict(vector_from_payload(d))[0])
