-- 01_schema.sql: Database Schemas and Table Definitions
-- DuckDB Analytical Warehouse for Indian Electric 2-Wheeler Market Intelligence

CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS stg;
CREATE SCHEMA IF NOT EXISTS mart;
CREATE SCHEMA IF NOT EXISTS kpi;
CREATE SCHEMA IF NOT EXISTS pending;

-- Drop existing views/tables to ensure clean initialization
DROP VIEW IF EXISTS mart_competitive_analysis;
DROP VIEW IF EXISTS mart_pricing_analysis;
DROP VIEW IF EXISTS mart_product_positioning;
DROP VIEW IF EXISTS kpi_status;
DROP TABLE IF EXISTS fact_product_metrics;
DROP TABLE IF EXISTS dim_product;
DROP TABLE IF EXISTS dim_manufacturer;
DROP TABLE IF EXISTS stg_verified_products;
DROP TABLE IF EXISTS sql_data_quality_results;
DROP TABLE IF EXISTS pending.fact_ev_registrations;
DROP VIEW IF EXISTS pending.market_queries_template;

-- STAGING: Verified Product Catalog
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

-- DIMENSION: Manufacturer
CREATE TABLE dim_manufacturer (
    manufacturer VARCHAR PRIMARY KEY,
    product_count BIGINT,
    priced_product_count BIGINT,
    min_price_inr DOUBLE,
    max_price_inr DOUBLE,
    avg_price_inr DOUBLE,
    median_price_inr DOUBLE,
    verification_status VARCHAR,
    source VARCHAR
);

-- DIMENSION: Product
CREATE TABLE dim_product (
    model_name VARCHAR PRIMARY KEY,
    manufacturer VARCHAR,
    vehicle_category VARCHAR,
    launch_status VARCHAR,
    price_basis VARCHAR,
    range_standard VARCHAR,
    source_url VARCHAR,
    source_type VARCHAR,
    accessed_date DATE,
    verification_status VARCHAR,
    verification_notes VARCHAR,
    source_dataset VARCHAR,
    provenance_class VARCHAR,
    source VARCHAR
);

-- FACT: Product Metrics & Analytical Ratios
CREATE TABLE fact_product_metrics (
    model_name VARCHAR PRIMARY KEY,
    manufacturer VARCHAR,
    vehicle_category VARCHAR,
    ex_showroom_price_inr DOUBLE,
    battery_capacity_kwh DOUBLE,
    range_km DOUBLE,
    top_speed_kmh DOUBLE,
    motor_peak_power_kw DOUBLE,
    price_per_km DOUBLE,
    price_per_kwh DOUBLE,
    wh_per_km DOUBLE,
    verification_status VARCHAR,
    source VARCHAR
);

-- DATA QUALITY RESULTS TABLE
CREATE TABLE sql_data_quality_results (
    check_name VARCHAR PRIMARY KEY,
    issue_count BIGINT,
    description VARCHAR,
    validation_date DATE
);
