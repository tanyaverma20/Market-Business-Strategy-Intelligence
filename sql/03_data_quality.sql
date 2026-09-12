CREATE OR REPLACE TABLE sql_data_quality_results AS
WITH base AS (
    SELECT *
    FROM stg_verified_products
),
checks AS (
    SELECT 'duplicate_products' AS check_name,
           COUNT(*) AS issue_count,
           'manufacturer + model_name duplicates' AS description
    FROM (
        SELECT manufacturer, model_name, COUNT(*) AS cnt
        FROM base
        GROUP BY manufacturer, model_name
        HAVING COUNT(*) > 1
    )

    UNION ALL
    SELECT 'null_required_fields' AS check_name,
           COUNT(*) AS issue_count,
           'manufacturer, model_name, verification_status, and product metrics required' AS description
    FROM base
    WHERE manufacturer IS NULL
       OR model_name IS NULL
       OR verification_status IS NULL
       OR vehicle_category IS NULL

    UNION ALL
    SELECT 'negative_prices' AS check_name,
           COUNT(*) AS issue_count,
           'ex_showroom_price_inr < 0' AS description
    FROM base
    WHERE ex_showroom_price_inr IS NOT NULL AND ex_showroom_price_inr < 0

    UNION ALL
    SELECT 'invalid_battery_capacity' AS check_name,
           COUNT(*) AS issue_count,
           'battery_capacity_kwh <= 0 or null for verified product' AS description
    FROM base
    WHERE battery_capacity_kwh IS NOT NULL AND battery_capacity_kwh <= 0

    UNION ALL
    SELECT 'invalid_ranges' AS check_name,
           COUNT(*) AS issue_count,
           'range_km <= 0 or null for verified product' AS description
    FROM base
    WHERE range_km IS NOT NULL AND range_km <= 0

    UNION ALL
    SELECT 'invalid_speed_values' AS check_name,
           COUNT(*) AS issue_count,
           'top_speed_kmh <= 0 or null for verified product' AS description
    FROM base
    WHERE top_speed_kmh IS NOT NULL AND top_speed_kmh <= 0

    UNION ALL
    SELECT 'invalid_motor_power' AS check_name,
           COUNT(*) AS issue_count,
           'motor_peak_power_kw <= 0 or null for verified product' AS description
    FROM base
    WHERE motor_peak_power_kw IS NOT NULL AND motor_peak_power_kw <= 0

    UNION ALL
    SELECT 'unverified_records' AS check_name,
           COUNT(*) AS issue_count,
           'verification_status != verified' AS description
    FROM base
    WHERE verification_status IS NOT NULL AND verification_status <> 'verified'

    UNION ALL
    SELECT 'missing_provenance' AS check_name,
           COUNT(*) AS issue_count,
           'missing source_url or source_dataset' AS description
    FROM base
    WHERE source_url IS NULL OR source_dataset IS NULL
)
SELECT check_name, issue_count, description, CURRENT_DATE AS validation_date
FROM checks;
