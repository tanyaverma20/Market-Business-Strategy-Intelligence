CREATE SCHEMA IF NOT EXISTS pending;

CREATE TABLE pending.fact_ev_registrations (
    date DATE,
    month INTEGER,
    year INTEGER,
    state VARCHAR,
    vehicle_category VARCHAR,
    fuel_type VARCHAR,
    manufacturer VARCHAR,
    registrations DOUBLE,
    source VARCHAR,
    verification_status VARCHAR DEFAULT 'PENDING VERIFIED DATA'
);

-- The table exists only as a schema placeholder for future validated Vahan data.
-- No rows are inserted. This is fail-closed and does not create factual market analytics.

CREATE OR REPLACE VIEW pending.market_queries_template AS
SELECT
    'annual_market_volume' AS query_name,
    'PENDING VERIFIED VAHAN DATA' AS status,
    'Expected fields: date, month, year, state, vehicle_category, fuel_type, manufacturer, registrations, source, verification_status' AS expected_schema

UNION ALL
SELECT
    'monthly_market_volume',
    'PENDING VERIFIED VAHAN DATA',
    'Requires verified Vahan monthly registration exports'

UNION ALL
SELECT
    'yoy_growth',
    'PENDING VERIFIED VAHAN DATA',
    'Requires verified annual market volume by year'

UNION ALL
SELECT
    'cagr',
    'PENDING VERIFIED VAHAN DATA',
    'Requires verified multi-year series'

UNION ALL
SELECT
    'ev_penetration',
    'PENDING VERIFIED VAHAN DATA',
    'Requires verified total_2w_registrations and EV volume'

UNION ALL
SELECT
    'oem_market_share',
    'PENDING VERIFIED VAHAN DATA',
    'Requires verified OEM registration series'

UNION ALL
SELECT
    'hhi',
    'PENDING VERIFIED VAHAN DATA',
    'Requires verified OEM market shares'

UNION ALL
SELECT
    'state_ranking',
    'PENDING VERIFIED VAHAN DATA',
    'Requires verified state-level market data';
