CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS stg;
CREATE SCHEMA IF NOT EXISTS mart;
CREATE SCHEMA IF NOT EXISTS kpi;
CREATE SCHEMA IF NOT EXISTS pending;

DROP TABLE IF EXISTS stg_verified_products;
DROP TABLE IF EXISTS dim_manufacturer;
DROP TABLE IF EXISTS dim_product;
DROP VIEW IF EXISTS mart_competitive_analysis;
DROP VIEW IF EXISTS mart_pricing_analysis;
DROP VIEW IF EXISTS mart_product_positioning;
DROP VIEW IF EXISTS kpi_status;
DROP TABLE IF EXISTS sql_data_quality_results;
DROP TABLE IF EXISTS pending_market_templates;

CREATE TABLE stg_verified_products (
    manufacturer VARCHAR,
    model_name VARCHAR,
    vehicle_category VARCHAR,
    ex_showroom_price_inr DOUBLE,
    price_basis VARCHAR,
    battery_capacity_kwh DOUBLE,
    range_km DOUBLE,
    range_standard VARCHAR,
    top_speed_kmh DOUBLE,
    motor_peak_power_kw DOUBLE,
    launch_status VARCHAR,
    source_url VARCHAR,
    source_type VARCHAR,
    accessed_date DATE,
    verification_status VARCHAR,
    verification_notes VARCHAR,
    source_dataset VARCHAR,
    provenance_class VARCHAR,
    eligible_as_observed_analytics VARCHAR,
    source VARCHAR DEFAULT 'verified_product_catalog_2025_2026.csv'
);

CREATE TABLE dim_manufacturer AS
SELECT DISTINCT
    manufacturer,
    'verified' AS verification_status,
    'verified_product_catalog_2025_2026.csv' AS source
FROM stg_verified_products
WHERE manufacturer IS NOT NULL;

CREATE TABLE dim_product AS
SELECT
    manufacturer,
    model_name,
    vehicle_category,
    ex_showroom_price_inr,
    battery_capacity_kwh,
    range_km,
    top_speed_kmh,
    motor_peak_power_kw,
    source_dataset,
    verification_status,
    source_url,
    accessed_date,
    source
FROM stg_verified_products;
