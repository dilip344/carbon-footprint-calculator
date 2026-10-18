from pathlib import Path
import json
import pandas as pd
from preprocessing import FEATURES

ROOT = Path(__file__).resolve().parent
DATA = ROOT.parent / "datasets" / "carbon_data.csv"
OUT = ROOT / "training_stats.json"

df = pd.read_csv(DATA)
means = df[FEATURES].mean().tolist()
stds = df[FEATURES].std().replace(0, 1e-6).fillna(1e-6).tolist()

with open(OUT, "w", encoding="utf-8") as f:
    json.dump({"mean": means, "std": stds, "features": FEATURES}, f, indent=2)

print(f"Saved {OUT}")
