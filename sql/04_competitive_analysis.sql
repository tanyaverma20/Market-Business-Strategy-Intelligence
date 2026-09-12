CREATE OR REPLACE VIEW mart_competitive_analysis AS
WITH product_metrics AS (
    SELECT
        manufacturer,
        model_name,
        vehicle_category AS category,
        ex_showroom_price_inr AS price,
        battery_capacity_kwh AS battery_kwh,
        range_km AS certified_range_km,
        top_speed_kmh AS top_speed_kmph,
        motor_peak_power_kw AS motor_power_kw,
        ex_showroom_price_inr / NULLIF(range_km, 0) AS price_per_km,
        ex_showroom_price_inr / NULLIF(battery_capacity_kwh, 0) AS price_per_kwh,
        verification_status,
        ROW_NUMBER() OVER (PARTITION BY manufacturer ORDER BY ex_showroom_price_inr ASC, model_name) AS manufacturer_rank,
        ROW_NUMBER() OVER (ORDER BY ex_showroom_price_inr ASC, model_name) AS product_rank,
        DENSE_RANK() OVER (PARTITION BY manufacturer ORDER BY ex_showroom_price_inr) AS price_dense_rank,
        RANK() OVER (ORDER BY ex_showroom_price_inr DESC) AS price_rank_desc
    FROM stg_verified_products
    WHERE verification_status = 'verified'
)
SELECT *
FROM product_metrics
ORDER BY manufacturer, price DESC, model_name;
