from pathlib import Path
import joblib
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from ai.preprocessing import FEATURES, vector_from_payload

ROOT = Path(__file__).resolve().parent
DATA = ROOT.parent / "datasets" / "carbon_data.csv"
OUT = ROOT / "trained_models"
OUT.mkdir(exist_ok=True)
PATH = OUT / "clustering.joblib"

LABELS = ["Low-impact lifestyle", "Moderate-impact lifestyle", "High-impact lifestyle"]


def train():
    df = pd.read_csv(DATA)
    scaler = StandardScaler()
    X = scaler.fit_transform(df[FEATURES])
    model = KMeans(n_clusters=3, n_init=10, random_state=42)
    model.fit(X)
    joblib.dump((scaler, model), PATH)
    return scaler, model


def get_model():
    return joblib.load(PATH) if PATH.exists() else train()


def predict_cluster_id(d):
    scaler, model = get_model()
    return int(model.predict(scaler.transform(vector_from_payload(d)))[0])


def cluster_label(cluster_id):
    scaler, model = get_model()
    centers = model.cluster_centers_.mean(axis=1)
    rank = sorted(range(len(centers)), key=lambda i: centers[i]).index(cluster_id)
    return LABELS[rank]


def predict_cluster(d):
    return cluster_label(predict_cluster_id(d))
