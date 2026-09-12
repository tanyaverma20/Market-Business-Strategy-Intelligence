CREATE OR REPLACE TABLE stg_verified_products AS
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

CREATE OR REPLACE TABLE dim_manufacturer AS
SELECT
    manufacturer,
    COUNT(*) AS product_count,
    MIN(ex_showroom_price_inr) AS min_price_inr,
    MAX(ex_showroom_price_inr) AS max_price_inr,
    AVG(ex_showroom_price_inr) AS avg_price_inr,
    'verified' AS verification_status,
    'verified_product_catalog_2025_2026.csv' AS source
FROM stg_verified_products
WHERE manufacturer IS NOT NULL
GROUP BY manufacturer;

CREATE OR REPLACE TABLE dim_product AS
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
FROM stg_verified_products
WHERE verification_status = 'verified';
