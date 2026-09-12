-- 07_kpi_queries.sql: Verified KPI Analytics Layer
-- Formats calculable verified product metrics, benchmarks, and portfolio intensity

CREATE OR REPLACE VIEW kpi_status AS
WITH mfg_shares AS (
    SELECT
        manufacturer,
        COUNT(*) * 100.0 / (SELECT COUNT(*) FROM stg_verified_products WHERE verification_status = 'verified') AS share_pct
    FROM stg_verified_products
    WHERE verification_status = 'verified'
    GROUP BY manufacturer
),
hhi_calc AS (
    SELECT ROUND(SUM(POW(share_pct, 2)), 2) AS catalog_hhi
    FROM mfg_shares
),
metrics AS (
    SELECT
        'manufacturer_count' AS kpi_name,
        ROUND(CAST(COUNT(DISTINCT manufacturer) AS DOUBLE), 2) AS value,
        'count' AS unit,
        'verified_product_catalog_2025_2026.csv' AS source,
        'verified' AS verification_status,
        CURRENT_DATE AS calculation_date,
        'COUNT(DISTINCT manufacturer) across verified products' AS methodology
    FROM stg_verified_products
    WHERE verification_status = 'verified'

    UNION ALL
    SELECT
        'product_count',
        ROUND(CAST(COUNT(*) AS DOUBLE), 2),
        'count',
        'verified_product_catalog_2025_2026.csv',
        'verified',
        CURRENT_DATE,
        'COUNT(*) across verified products'
    FROM stg_verified_products
    WHERE verification_status = 'verified'

    UNION ALL
    SELECT
        'priced_product_count',
        ROUND(CAST(COUNT(ex_showroom_price_inr) AS DOUBLE), 2),
        'count',
        'verified_product_catalog_2025_2026.csv',
        'verified',
        CURRENT_DATE,
        'COUNT(ex_showroom_price_inr) with verified pricing'
    FROM stg_verified_products
    WHERE verification_status = 'verified'

    UNION ALL
    SELECT
        'average_price_inr',
        ROUND(AVG(ex_showroom_price_inr), 2),
        'INR',
        'verified_product_catalog_2025_2026.csv',
        'verified',
        CURRENT_DATE,
        'AVG(ex_showroom_price_inr) across priced models'
    FROM stg_verified_products
    WHERE verification_status = 'verified' AND ex_showroom_price_inr IS NOT NULL

    UNION ALL
    SELECT
        'median_price_inr',
        ROUND(MEDIAN(ex_showroom_price_inr), 2),
        'INR',
        'verified_product_catalog_2025_2026.csv',
        'verified',
        CURRENT_DATE,
        'MEDIAN(ex_showroom_price_inr) across priced models'
    FROM stg_verified_products
    WHERE verification_status = 'verified' AND ex_showroom_price_inr IS NOT NULL

    UNION ALL
    SELECT
        'min_price_inr',
        ROUND(MIN(ex_showroom_price_inr), 2),
        'INR',
        'verified_product_catalog_2025_2026.csv',
        'verified',
        CURRENT_DATE,
        'MIN(ex_showroom_price_inr) in verified catalog'
    FROM stg_verified_products
    WHERE verification_status = 'verified' AND ex_showroom_price_inr IS NOT NULL

    UNION ALL
    SELECT
        'max_price_inr',
        ROUND(MAX(ex_showroom_price_inr), 2),
        'INR',
        'verified_product_catalog_2025_2026.csv',
        'verified',
        CURRENT_DATE,
        'MAX(ex_showroom_price_inr) in verified catalog'
    FROM stg_verified_products
    WHERE verification_status = 'verified' AND ex_showroom_price_inr IS NOT NULL

    UNION ALL
    SELECT
        'average_battery_kwh',
        ROUND(AVG(battery_capacity_kwh), 2),
        'kWh',
        'verified_product_catalog_2025_2026.csv',
        'verified',
        CURRENT_DATE,
        'AVG(battery_capacity_kwh) across models'
    FROM stg_verified_products
    WHERE verification_status = 'verified' AND battery_capacity_kwh IS NOT NULL

    UNION ALL
    SELECT
        'average_range_km',
        ROUND(AVG(range_km), 2),
        'km',
        'verified_product_catalog_2025_2026.csv',
        'verified',
        CURRENT_DATE,
        'AVG(range_km) across models with verified range'
    FROM stg_verified_products
    WHERE verification_status = 'verified' AND range_km IS NOT NULL

    UNION ALL
    SELECT
        'average_top_speed_kmh',
        ROUND(AVG(top_speed_kmh), 2),
        'km/h',
        'verified_product_catalog_2025_2026.csv',
        'verified',
        CURRENT_DATE,
        'AVG(top_speed_kmh) across models with verified speed'
    FROM stg_verified_products
    WHERE verification_status = 'verified' AND top_speed_kmh IS NOT NULL

    UNION ALL
    SELECT
        'average_motor_power_kw',
        ROUND(AVG(motor_peak_power_kw), 2),
        'kW',
        'verified_product_catalog_2025_2026.csv',
        'verified',
        CURRENT_DATE,
        'AVG(motor_peak_power_kw) across models with verified motor power'
    FROM stg_verified_products
    WHERE verification_status = 'verified' AND motor_peak_power_kw IS NOT NULL

    UNION ALL
    SELECT
        'average_price_per_km',
        ROUND(AVG(ex_showroom_price_inr / NULLIF(range_km, 0)), 2),
        'INR/km',
        'verified_product_catalog_2025_2026.csv',
        'verified',
        CURRENT_DATE,
        'AVG(price / range) for priced models with certified range'
    FROM stg_verified_products
    WHERE verification_status = 'verified' AND ex_showroom_price_inr IS NOT NULL AND range_km IS NOT NULL

    UNION ALL
    SELECT
        'average_price_per_kwh',
        ROUND(AVG(ex_showroom_price_inr / NULLIF(battery_capacity_kwh, 0)), 2),
        'INR/kWh',
        'verified_product_catalog_2025_2026.csv',
        'verified',
        CURRENT_DATE,
        'AVG(price / battery_capacity) for priced models'
    FROM stg_verified_products
    WHERE verification_status = 'verified' AND ex_showroom_price_inr IS NOT NULL AND battery_capacity_kwh IS NOT NULL

    UNION ALL
    SELECT
        'product_portfolio_hhi',
        catalog_hhi,
        'index',
        'verified_product_catalog_2025_2026.csv',
        'verified',
        CURRENT_DATE,
        'SUM(portfolio_share^2) measuring OEM product offering concentration'
    FROM hhi_calc
)
SELECT *
FROM metrics;
