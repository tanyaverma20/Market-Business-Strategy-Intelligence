-- 04_competitive_analysis.sql: Competitive Analysis Mart
-- Compares OEM portfolios, specifications, price efficiency, and rankings

CREATE OR REPLACE VIEW mart_competitive_analysis AS
WITH base AS (
    SELECT
        manufacturer,
        model_name AS product,
        vehicle_category AS category,
        ex_showroom_price_inr AS price,
        battery_capacity_kwh AS battery_kwh,
        range_km AS certified_range_km,
        top_speed_kmh AS top_speed_kmph,
        motor_peak_power_kw AS motor_power_kw,
        ROUND(ex_showroom_price_inr / NULLIF(range_km, 0), 2) AS price_per_km,
        ROUND(ex_showroom_price_inr / NULLIF(battery_capacity_kwh, 0), 2) AS price_per_kwh,
        verification_status
    FROM stg_verified_products
    WHERE verification_status = 'verified'
),
ranked AS (
    SELECT
        *,
        -- Window function: Rank within manufacturer by price
        ROW_NUMBER() OVER (
            PARTITION BY manufacturer 
            ORDER BY price ASC NULLS LAST, product
        ) AS mfg_price_rank,
        -- Window function: Overall product price rank
        DENSE_RANK() OVER (
            ORDER BY price ASC NULLS LAST
        ) AS overall_price_rank,
        -- Window function: Price efficiency rank (lowest cost per km)
        RANK() OVER (
            ORDER BY price_per_km ASC NULLS LAST
        ) AS price_efficiency_rank,
        -- Window function: Range rank (longest range)
        RANK() OVER (
            ORDER BY certified_range_km DESC NULLS LAST
        ) AS range_rank,
        -- Window function: Speed rank (highest top speed)
        RANK() OVER (
            ORDER BY top_speed_kmph DESC NULLS LAST
        ) AS speed_rank,
        -- Window function: Manufacturer portfolio count and portfolio share
        COUNT(*) OVER (PARTITION BY manufacturer) AS mfg_product_count,
        ROUND(100.0 * COUNT(*) OVER (PARTITION BY manufacturer) / COUNT(*) OVER (), 1) AS mfg_portfolio_share_pct
    FROM base
)
SELECT
    manufacturer,
    product,
    category,
    price,
    battery_kwh,
    certified_range_km,
    top_speed_kmph,
    motor_power_kw,
    price_per_km,
    price_per_kwh,
    mfg_price_rank AS manufacturer_rank,
    overall_price_rank AS product_rank,
    price_efficiency_rank,
    range_rank,
    speed_rank,
    mfg_product_count,
    mfg_portfolio_share_pct,
    verification_status
FROM ranked;
