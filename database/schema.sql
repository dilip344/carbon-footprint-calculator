CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(160) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE carbon_records (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    user_name VARCHAR(120),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    mode VARCHAR(20) NOT NULL DEFAULT 'individual',
    entity_name VARCHAR(160),
    population INTEGER NOT NULL DEFAULT 1,
    travel_mode VARCHAR(30),
    travel_km FLOAT,
    fuel_liters FLOAT,
    electricity_kwh FLOAT,
    lpg_kg FLOAT,
    water_liters FLOAT,
    waste_kg FLOAT,
    food_type VARCHAR(30),
    flights FLOAT,
    paper_kg FLOAT,
    trees INTEGER,
    monthly_emissions FLOAT,
    annual_emissions FLOAT,
    sustainability_score FLOAT,
    cluster VARCHAR(100),
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE fusion_records (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    carbon_record_id INTEGER,
    cluster_id INTEGER,
    deterministic_value FLOAT,
    ml_value FLOAT,
    fused_value FLOAT,
    confidence_weight FLOAT,
    s1_distance FLOAT,
    s2_density FLOAT,
    s3_residual FLOAT,
    divergence_flag BOOLEAN DEFAULT 0,
    dynamic_threshold FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(carbon_record_id) REFERENCES carbon_records(id)
);

CREATE TABLE cluster_residual_stats (
    cluster_id INTEGER PRIMARY KEY,
    mean_abs_error FLOAT DEFAULT 0,
    sample_count INTEGER DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
