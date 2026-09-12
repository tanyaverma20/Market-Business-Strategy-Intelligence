CREATE OR REPLACE VIEW kpi_status AS
WITH metrics AS (
    SELECT
        'manufacturer_count' AS kpi_name,
        CAST(COUNT(DISTINCT manufacturer) AS BIGINT) AS value,
        'count' AS unit,
        'verified_product_catalog_2025_2026.csv' AS source,
        'verified' AS verification_status,
        CURRENT_DATE AS calculation_date,
        'COUNT(DISTINCT manufacturer) from verified products' AS methodology
    FROM stg_verified_products
    WHERE verification_status = 'verified'

    UNION ALL
    SELECT
        'product_count',
        CAST(COUNT(*) AS BIGINT),
        'count',
        'verified_product_catalog_2025_2026.csv',
        'verified',
        CURRENT_DATE,
        'COUNT(*) from verified products'
    FROM stg_verified_products
    WHERE verification_status = 'verified'

    UNION ALL
    SELECT
        'average_price_inr',
        AVG(ex_showroom_price_inr),
        'INR',
        'verified_product_catalog_2025_2026.csv',
        'verified',
        CURRENT_DATE,
        'AVG(ex_showroom_price_inr) from verified products'
    FROM stg_verified_products
    WHERE verification_status = 'verified' AND ex_showroom_price_inr IS NOT NULL

    UNION ALL
    SELECT
        'average_battery_kwh',
        AVG(battery_capacity_kwh),
        'kWh',
        'verified_product_catalog_2025_2026.csv',
        'verified',
        CURRENT_DATE,
        'AVG(battery_capacity_kwh) from verified products'
    FROM stg_verified_products
    WHERE verification_status = 'verified' AND battery_capacity_kwh IS NOT NULL

    UNION ALL
    SELECT
        'average_range_km',
        AVG(range_km),
        'km',
        'verified_product_catalog_2025_2026.csv',
        'verified',
        CURRENT_DATE,
        'AVG(range_km) from verified products'
    FROM stg_verified_products
    WHERE verification_status = 'verified' AND range_km IS NOT NULL

    UNION ALL
    SELECT
        'average_top_speed_kmh',
        AVG(top_speed_kmh),
        'km/h',
        'verified_product_catalog_2025_2026.csv',
        'verified',
        CURRENT_DATE,
        'AVG(top_speed_kmh) from verified products'
    FROM stg_verified_products
    WHERE verification_status = 'verified' AND top_speed_kmh IS NOT NULL

    UNION ALL
    SELECT
        'average_motor_power_kw',
        AVG(motor_peak_power_kw),
        'kW',
        'verified_product_catalog_2025_2026.csv',
        'verified',
        CURRENT_DATE,
        'AVG(motor_peak_power_kw) from verified products'
    FROM stg_verified_products
    WHERE verification_status = 'verified' AND motor_peak_power_kw IS NOT NULL
)
SELECT *
FROM metrics;
