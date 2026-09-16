-- 05_pricing_analysis.sql: Pricing Mart
-- Computes price distributions, percentiles, quartiles, and relative market positioning

CREATE OR REPLACE VIEW mart_pricing_analysis AS
WITH ranked AS (
    SELECT
        manufacturer,
        model_name AS product,
        ex_showroom_price_inr AS price,
        battery_capacity_kwh,
        range_km,
        top_speed_kmh,
        ROUND(ex_showroom_price_inr / NULLIF(range_km, 0), 2) AS price_per_km,
        ROUND(ex_showroom_price_inr / NULLIF(battery_capacity_kwh, 0), 2) AS price_per_kwh,
        -- Window function: Percentile ranking across priced catalog (0.0 to 1.0)
        ROUND(PERCENT_RANK() OVER (
            PARTITION BY CASE WHEN ex_showroom_price_inr IS NOT NULL THEN 1 ELSE 0 END 
            ORDER BY ex_showroom_price_inr
        ), 2) AS price_percentile,
        -- Window function: Quartile segmentation (1 = Lowest 25%, 4 = Highest 25%)
        NTILE(4) OVER (
            PARTITION BY CASE WHEN ex_showroom_price_inr IS NOT NULL THEN 1 ELSE 0 END 
            ORDER BY ex_showroom_price_inr
        ) AS price_quartile,
        -- Window function: Product price rank descending
        RANK() OVER (ORDER BY ex_showroom_price_inr DESC NULLS LAST) AS product_price_rank,
        -- Window function: Value rank (lowest price per km)
        RANK() OVER (
            ORDER BY ROUND(ex_showroom_price_inr / NULLIF(range_km, 0), 2) ASC NULLS LAST
        ) AS value_rank,
        -- Window function: Overall catalog average price
        ROUND(AVG(ex_showroom_price_inr) OVER (), 2) AS avg_market_price,
        -- Window function: Manufacturer average price
        ROUND(AVG(ex_showroom_price_inr) OVER (PARTITION BY manufacturer), 2) AS mfg_avg_price
    FROM stg_verified_products
    WHERE verification_status = 'verified'
)
SELECT
    product,
    manufacturer,
    price,
    battery_capacity_kwh,
    range_km,
    top_speed_kmh,
    price_per_km,
    price_per_kwh,
    CASE
        WHEN price IS NULL THEN 'unpriced'
        WHEN price < 100000 THEN 'budget'
        WHEN price <= 180000 THEN 'mid-market'
        ELSE 'premium'
    END AS price_bucket,
    value_rank,
    price_percentile,
    price_quartile,
    product_price_rank,
    avg_market_price,
    mfg_avg_price,
    CASE
        WHEN price IS NULL THEN 'unpriced / pending'
        WHEN price < avg_market_price THEN 'below market average'
        WHEN price > avg_market_price THEN 'above market average'
        ELSE 'at market average'
    END AS relative_price_position,
    CASE
        WHEN price IS NOT NULL AND avg_market_price IS NOT NULL
        THEN ROUND(100.0 * (price - avg_market_price) / avg_market_price, 1)
        ELSE NULL
    END AS price_premium_vs_market_pct
FROM ranked;
