-- 02_load_verified_data.sql: Ingestion and Provenance Enforcement
-- Loads verified product catalog into staging, dimensions, and facts

DELETE FROM stg_verified_products;

INSERT INTO stg_verified_products (
    manufacturer,
    model_name,
    vehicle_category,
    ex_showroom_price_inr,
    price_basis,
    battery_capacity_kwh,
    range_km,
    range_standard,
    top_speed_kmh,
    motor_peak_power_kw,
    launch_status,
    source_url,
    source_type,
    accessed_date,
    verification_status,
    verification_notes,
    source_dataset,
    provenance_class,
    eligible_as_observed_analytics,
    source
)
SELECT
    manufacturer,
    model_name,
    vehicle_category,
    CAST(ex_showroom_price_inr AS DOUBLE) AS ex_showroom_price_inr,
    price_basis,
    CAST(battery_capacity_kwh AS DOUBLE) AS battery_capacity_kwh,
    CAST(range_km AS DOUBLE) AS range_km,
    range_standard,
    CAST(top_speed_kmh AS DOUBLE) AS top_speed_kmh,
    CAST(motor_peak_power_kw AS DOUBLE) AS motor_peak_power_kw,
    launch_status,
    source_url,
    source_type,
    CAST(accessed_date AS DATE) AS accessed_date,
    verification_status,
    verification_notes,
    source_dataset,
    provenance_class,
    eligible_as_observed_analytics,
    'verified_product_catalog_2025_2026.csv' AS source
FROM read_csv_auto('data/processed/processed_verified_product_catalog.csv', header = true, all_varchar = false);

-- Populate dim_manufacturer
DELETE FROM dim_manufacturer;

INSERT INTO dim_manufacturer (
    manufacturer,
    product_count,
    priced_product_count,
    min_price_inr,
    max_price_inr,
    avg_price_inr,
    median_price_inr,
    verification_status,
    source
)
SELECT
    manufacturer,
    COUNT(*) AS product_count,
    COUNT(ex_showroom_price_inr) AS priced_product_count,
    MIN(ex_showroom_price_inr) AS min_price_inr,
    MAX(ex_showroom_price_inr) AS max_price_inr,
    ROUND(AVG(ex_showroom_price_inr), 2) AS avg_price_inr,
    ROUND(MEDIAN(ex_showroom_price_inr), 2) AS median_price_inr,
    'verified' AS verification_status,
    'verified_product_catalog_2025_2026.csv' AS source
FROM stg_verified_products
WHERE verification_status = 'verified' AND manufacturer IS NOT NULL
GROUP BY manufacturer;

-- Populate dim_product
DELETE FROM dim_product;

INSERT INTO dim_product (
    model_name,
    manufacturer,
    vehicle_category,
    launch_status,
    price_basis,
    range_standard,
    source_url,
    source_type,
    accessed_date,
    verification_status,
    verification_notes,
    source_dataset,
    provenance_class,
    source
)
SELECT
    model_name,
    manufacturer,
    vehicle_category,
    launch_status,
    price_basis,
    range_standard,
    source_url,
    source_type,
    accessed_date,
    verification_status,
    verification_notes,
    source_dataset,
    provenance_class,
    source
FROM stg_verified_products
WHERE verification_status = 'verified';

-- Populate fact_product_metrics
DELETE FROM fact_product_metrics;

INSERT INTO fact_product_metrics (
    model_name,
    manufacturer,
    vehicle_category,
    ex_showroom_price_inr,
    battery_capacity_kwh,
    range_km,
    top_speed_kmh,
    motor_peak_power_kw,
    price_per_km,
    price_per_kwh,
    wh_per_km,
    verification_status,
    source
)
SELECT
    model_name,
    manufacturer,
    vehicle_category,
    ex_showroom_price_inr,
    battery_capacity_kwh,
    range_km,
    top_speed_kmh,
    motor_peak_power_kw,
    ROUND(ex_showroom_price_inr / NULLIF(range_km, 0), 2) AS price_per_km,
    ROUND(ex_showroom_price_inr / NULLIF(battery_capacity_kwh, 0), 2) AS price_per_kwh,
    ROUND((battery_capacity_kwh * 1000.0) / NULLIF(range_km, 0), 2) AS wh_per_km,
    verification_status,
    source
FROM stg_verified_products
WHERE verification_status = 'verified';
