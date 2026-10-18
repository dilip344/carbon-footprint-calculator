# GreenPulse Project (carbon-footprint-calculator)

GreenPulse is a web-based carbon footprint platform with two modes:

- **Individual Mode** — personal lifestyle footprint, score, history, recommendations and forecast.
- **Community Mode** — campus, NGO, school, village, office or other group footprint with population and per-person impact.

The project is organized into three integrated layers:

1. **Frontend** — React + Vite + Recharts, with the premium GreenPulse dashboard design.
2. **AI / Data** — deterministic calculation + Random Forest + K-Means + Adaptive Hybrid Emission Fusion + forecasting + recommendations.
3. **Backend** — FastAPI + SQLAlchemy + SQLite + PDF reporting + authentication.

## Technology

Frontend:
- React 19
- Vite
- Recharts
- Responsive CSS dashboard

Backend:
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- ReportLab for PDF reports
- scikit-learn for prediction, clustering and forecasting

## Main features

### Individual Mode
- Registration and login
- Personal carbon calculator
- Monthly and annual emissions
- Emission-source breakdown
- Sustainability score
- AI lifestyle clustering
- AI annual prediction
- Six-month forecast
- Personalized recommendations
- History and downloadable PDF reports

### Community Mode
- Community/campus/NGO name
- Number of people/members
- Aggregate monthly transport, fuel, electricity, LPG, water, waste, paper and flight inputs
- Food-pattern estimation across the group
- Tree-plantation offset
- Total community emissions
- Per-person monthly and annual impact
- AI community pattern
- AI prediction and forecast
- Community-specific recommendations
- Separate history and PDF reports

## Folder structure

```text
GreenPulse_Final/
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models/
│   ├── schemas/
│   ├── routes/
│   ├── services/
│   └── requirements.txt
├── ai/
│   ├── prediction_model.py
│   ├── clustering_model.py
│   ├── forecasting_model.py
│   ├── compute_training_stats.py
│   ├── training_stats.json
│   └── trained_models/
├── datasets/
│   └── carbon_data.csv
└── database/
    └── schema.sql
```

## Requirements

- Python 3.12 recommended
- Conda environment recommended: `carbon-ai`
- Node.js + npm

## 1. Backend

Open PowerShell:

```powershell
conda activate carbon-ai
cd GreenPulse_Final\backend
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/health
```

The SQLite database is created automatically at:

```text
backend/carbon.db
```

Do not delete this database if you want to keep user accounts and calculation history.

## 2. Frontend

Open another PowerShell window:

```powershell
cd GreenPulse_Final\frontend
npm install
npm run dev
```

Open:

```text
http://localhost:5173
```

The frontend expects the FastAPI server at `http://127.0.0.1:8000`.

## Main API routes

```text
POST /api/auth/register
POST /api/auth/login
POST /api/carbon/calculate/{uid}
GET  /api/carbon/latest/{uid}?mode=individual|community
GET  /api/carbon/history/{uid}?mode=individual|community
GET  /api/carbon/fusion/{uid}?mode=individual|community
GET  /api/carbon/report/{rid}
POST /api/community/calculate/{uid}
```

## AI pipeline

For every calculation:

```text
Input
  ↓
Deterministic calculation (D)
  +
Random Forest prediction (M)
  +
K-Means cluster
  ↓
Confidence signals S1, S2, S3
  ↓
Dynamic confidence weight w
  ↓
F = wM + (1-w)D
  ↓
Forecast + recommendations + sustainability score
  ↓
SQLite
```

The fusion record stores D, M, F, confidence weight, S1, S2, S3, cluster and divergence information.

## Important database tables

```text
users
carbon_records
fusion_records
cluster_residual_stats
```

`carbon_records` stores both Individual and Community calculations. `fusion_records` stores the transparent AI/fusion details for each calculation.

## Notes

- `node_modules` is intentionally not included. Run `npm install` on Windows.
- A fresh `carbon.db` is intentionally not included; the backend creates it automatically.
- Existing older `carbon.db` files are migrated by the backend where supported.
- The application is a web application, not a mobile application.
