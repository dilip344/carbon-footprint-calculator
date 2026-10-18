import os
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine, ensure_schema
from models.carbon import CarbonRecord
from models.fusion import ClusterResidualStats, FusionRecord
from models.user import User
from routes.auth import router as auth_router
from routes.carbon import router as carbon_router
from routes.community import router as community_router

Base.metadata.create_all(bind=engine)
ensure_schema()

app = FastAPI(
    title="GreenPulse Backend",
    description="Backend API for individual and sustainable-community carbon footprint analysis.",
    version="4.0.0",
)

origins = [
    item.strip()
    for item in os.getenv(
        "GREENPULSE_FRONTEND_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if item.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(carbon_router)
app.include_router(community_router)


@app.get("/")
def root():
    return {
        "project": "GreenPulse",
        "status": "running",
        "version": "4.0.0",
        "modes": ["individual", "community"],
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "ok", "database": "sqlite", "version": "4.0.0"}
