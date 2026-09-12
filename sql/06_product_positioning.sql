CREATE OR REPLACE VIEW mart_product_positioning AS
WITH base AS (
    SELECT
        manufacturer,
        model_name,
        ex_showroom_price_inr AS price,
        battery_capacity_kwh,
        range_km,
        top_speed_kmh,
        CASE
            WHEN ex_showroom_price_inr < 100000 THEN 'budget'
            WHEN ex_showroom_price_inr < 180000 THEN 'mid-market'
            ELSE 'premium'
        END AS price_bucket,
        CASE
            WHEN range_km < 120 THEN 'short-range'
            WHEN range_km < 180 THEN 'standard-range'
            ELSE 'long-range'
        END AS range_bucket,
        CASE
            WHEN battery_capacity_kwh < 3.0 THEN 'compact-battery'
            WHEN battery_capacity_kwh < 4.5 THEN 'standard-battery'
            ELSE 'high-battery'
        END AS battery_bucket,
        CASE
            WHEN top_speed_kmh < 70 THEN 'entry'
            WHEN top_speed_kmh < 90 THEN 'balanced'
            ELSE 'high-performance'
        END AS performance_bucket
    FROM stg_verified_products
    WHERE verification_status = 'verified'
)
SELECT
    manufacturer,
    model_name,
    price_bucket,
    range_bucket,
    battery_bucket,
    performance_bucket,
    CONCAT(price_bucket, ' / ', range_bucket) AS positioning_summary,
    ROW_NUMBER() OVER (PARTITION BY manufacturer ORDER BY price ASC, model_name) AS manufacturer_product_rank,
    SUM(CASE WHEN price_bucket = 'budget' THEN 1 ELSE 0 END) OVER (PARTITION BY manufacturer) AS manufacturer_budget_count,
    verification_status
FROM (
    SELECT b.*, 'verified' AS verification_status
    FROM base b
) q;
