-- 03_data_quality.sql: Data Quality Validation Rules
-- Enforces integrity, business rules, and provenance safeguards

DELETE FROM sql_data_quality_results;

INSERT INTO sql_data_quality_results (check_name, issue_count, description, validation_date)
WITH base AS (
    SELECT *
    FROM stg_verified_products
),
checks AS (
    SELECT
        'duplicate_products' AS check_name,
        COUNT(*) AS issue_count,
        'Duplicate model names across catalog' AS description
    FROM (
        SELECT model_name
        FROM base
        GROUP BY model_name
        HAVING COUNT(*) > 1
    )

    UNION ALL
    SELECT
        'duplicate_manufacturer_model' AS check_name,
        COUNT(*) AS issue_count,
        'Duplicate manufacturer and model_name combinations' AS description
    FROM (
        SELECT manufacturer, model_name
        FROM base
        GROUP BY manufacturer, model_name
        HAVING COUNT(*) > 1
    )

    UNION ALL
    SELECT
        'null_required_fields' AS check_name,
        COUNT(*) AS issue_count,
        'Null values in required fields: manufacturer, model_name, vehicle_category, verification_status' AS description
    FROM base
    WHERE manufacturer IS NULL
       OR model_name IS NULL
       OR vehicle_category IS NULL
       OR verification_status IS NULL

    UNION ALL
    SELECT
        'negative_prices' AS check_name,
        COUNT(*) AS issue_count,
        'Negative ex-showroom prices (< 0)' AS description
    FROM base
    WHERE ex_showroom_price_inr IS NOT NULL AND ex_showroom_price_inr < 0

    UNION ALL
    SELECT
        'invalid_battery_capacities' AS check_name,
        COUNT(*) AS issue_count,
        'Non-positive battery capacities (<= 0 kWh)' AS description
    FROM base
    WHERE battery_capacity_kwh IS NOT NULL AND battery_capacity_kwh <= 0

    UNION ALL
    SELECT
        'invalid_ranges' AS check_name,
        COUNT(*) AS issue_count,
        'Non-positive certified ranges (<= 0 km)' AS description
    FROM base
    WHERE range_km IS NOT NULL AND range_km <= 0

    UNION ALL
    SELECT
        'invalid_speed_values' AS check_name,
        COUNT(*) AS issue_count,
        'Non-positive top speed values (<= 0 km/h)' AS description
    FROM base
    WHERE top_speed_kmh IS NOT NULL AND top_speed_kmh <= 0

    UNION ALL
    SELECT
        'invalid_motor_power' AS check_name,
        COUNT(*) AS issue_count,
        'Non-positive motor peak power values (<= 0 kW)' AS description
    FROM base
    WHERE motor_peak_power_kw IS NOT NULL AND motor_peak_power_kw <= 0

    UNION ALL
    SELECT
        'unverified_records' AS check_name,
        COUNT(*) AS issue_count,
        'Records where verification_status != verified' AS description
    FROM base
    WHERE verification_status IS NULL OR verification_status <> 'verified'

    UNION ALL
    SELECT
        'missing_provenance' AS check_name,
        COUNT(*) AS issue_count,
        'Missing source_url, source_dataset, or accessed_date' AS description
    FROM base
    WHERE source_url IS NULL
       OR source_dataset IS NULL
       OR accessed_date IS NULL
)
SELECT
    check_name,
    issue_count,
    description,
    CURRENT_DATE AS validation_date
FROM checks;
