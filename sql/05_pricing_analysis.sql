CREATE OR REPLACE VIEW mart_pricing_analysis AS
WITH ranked AS (
    SELECT
        manufacturer,
        model_name AS product,
        ex_showroom_price_inr AS price,
        battery_capacity_kwh,
        range_km,
        top_speed_kmh,
        ex_showroom_price_inr / NULLIF(range_km, 0) AS price_per_km,
        ex_showroom_price_inr / NULLIF(battery_capacity_kwh, 0) AS price_per_kwh,
        PERCENT_RANK() OVER (ORDER BY ex_showroom_price_inr) AS price_percentile,
        NTILE(4) OVER (ORDER BY ex_showroom_price_inr) AS price_quartile,
        ROW_NUMBER() OVER (ORDER BY ex_showroom_price_inr DESC, manufacturer, model_name) AS product_price_rank,
        AVG(ex_showroom_price_inr) OVER () AS avg_market_price,
        SUM(ex_showroom_price_inr) OVER () AS total_market_price
    FROM stg_verified_products
    WHERE verification_status = 'verified'
)
SELECT
    manufacturer,
    product,
    price,
    battery_capacity_kwh,
    range_km,
    top_speed_kmh,
    price_per_km,
    price_per_kwh,
    price_percentile,
    price_quartile,
    product_price_rank,
    CASE
        WHEN price < AVG(avg_market_price) THEN 'below market average'
        WHEN price > AVG(avg_market_price) THEN 'above market average'
        ELSE 'at market average'
    END AS relative_price_position
FROM ranked;
