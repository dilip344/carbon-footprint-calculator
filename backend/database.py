from pathlib import Path
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import declarative_base, sessionmaker

BASE_DIR = Path(__file__).resolve().parent
DATABASE_URL = f"sqlite:///{BASE_DIR / 'carbon.db'}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def ensure_schema():
    """Create new tables and migrate older V2/V3 carbon.db files safely."""
    Base.metadata.create_all(bind=engine)
    inspector = inspect(engine)
    tables = set(inspector.get_table_names())

    if "carbon_records" in tables:
        columns = {c["name"] for c in inspector.get_columns("carbon_records")}
        additions = {
            "mode": "VARCHAR(20) DEFAULT 'individual'",
            "entity_name": "VARCHAR(160)",
            "population": "INTEGER DEFAULT 1",
        }
        with engine.begin() as conn:
            for name, definition in additions.items():
                if name not in columns:
                    conn.execute(text(f"ALTER TABLE carbon_records ADD COLUMN {name} {definition}"))
            conn.execute(text("UPDATE carbon_records SET mode='individual' WHERE mode IS NULL"))
            conn.execute(text("UPDATE carbon_records SET population=1 WHERE population IS NULL"))

    if "fusion_records" in tables:
        columns = {c["name"] for c in inspector.get_columns("fusion_records")}
        additions = {
            "carbon_record_id": "INTEGER",
            "dynamic_threshold": "FLOAT",
        }
        with engine.begin() as conn:
            for name, definition in additions.items():
                if name not in columns:
                    conn.execute(text(f"ALTER TABLE fusion_records ADD COLUMN {name} {definition}"))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
