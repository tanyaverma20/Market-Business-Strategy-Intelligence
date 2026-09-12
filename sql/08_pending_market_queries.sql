-- 08_pending_market_queries.sql: Fail-Closed Pending Market Data Schema & Future Analytical Templates
-- POLICY: The project lacks verified official Vahan registration exports.
-- In strict adherence to the project's provenance safeguard:
-- 1. fact_ev_registrations is created as an EMPTY table (0 rows).
-- 2. No proxy data is converted or loaded into factual SQL tables.
-- 3. Market queries are defined as templates/pending and documented below.

CREATE SCHEMA IF NOT EXISTS pending;

DROP TABLE IF EXISTS pending.fact_ev_registrations;

CREATE TABLE pending.fact_ev_registrations (
    date DATE,
    month INTEGER,
    year INTEGER,
    state VARCHAR,
    vehicle_category VARCHAR,
    fuel_type VARCHAR,
    manufacturer VARCHAR,
    registrations BIGINT,
    source VARCHAR,
    verification_status VARCHAR DEFAULT 'PENDING VERIFIED VAHAN DATA'
);

-- Template registry view documenting expected schema, prerequisites, and status
CREATE OR REPLACE VIEW pending.market_queries_template AS
SELECT
    'annual_market_volume' AS query_name,
    'PENDING VERIFIED VAHAN DATA' AS status,
    'SELECT year, SUM(registrations) FROM pending.fact_ev_registrations GROUP BY year' AS template_sql,
    'Requires verified Vahan annual registration export' AS data_prerequisite

UNION ALL
SELECT
    'monthly_market_volume',
    'PENDING VERIFIED VAHAN DATA',
    'SELECT year, month, SUM(registrations) FROM pending.fact_ev_registrations GROUP BY year, month ORDER BY year, month',
    'Requires verified Vahan monthly registration series'

UNION ALL
SELECT
    'yoy_growth',
    'PENDING VERIFIED VAHAN DATA',
    'WITH annual AS (SELECT year, SUM(registrations) AS vol FROM pending.fact_ev_registrations GROUP BY year) SELECT year, vol, ROUND(100.0 * (vol - LAG(vol) OVER (ORDER BY year)) / NULLIF(LAG(vol) OVER (ORDER BY year), 0), 2) AS yoy_growth_pct FROM annual',
    'Requires minimum 2 consecutive years of verified Vahan data'

UNION ALL
SELECT
    'cagr',
    'PENDING VERIFIED VAHAN DATA',
    'WITH bounds AS (SELECT MIN(year) AS start_yr, MAX(year) AS end_yr, FIRST_VALUE(vol) OVER (ORDER BY year ASC) AS v_start, FIRST_VALUE(vol) OVER (ORDER BY year DESC) AS v_end FROM (SELECT year, SUM(registrations) AS vol FROM pending.fact_ev_registrations GROUP BY year)) SELECT ROUND(100.0 * (POW(v_end * 1.0 / NULLIF(v_start, 0), 1.0 / NULLIF(end_yr - start_yr, 0)) - 1.0), 2) AS cagr_pct FROM bounds LIMIT 1',
    'Requires multi-year verified registration history'

UNION ALL
SELECT
    'ev_penetration',
    'PENDING VERIFIED VAHAN DATA',
    'SELECT year, ROUND(100.0 * SUM(CASE WHEN fuel_type = ''ELECTRIC'' THEN registrations ELSE 0 END) / NULLIF(SUM(registrations), 0), 2) AS ev_penetration_pct FROM pending.fact_ev_registrations GROUP BY year',
    'Requires total 2W registrations alongside EV registrations by year'

UNION ALL
SELECT
    'oem_market_share',
    'PENDING VERIFIED VAHAN DATA',
    'SELECT year, manufacturer, SUM(registrations) AS oem_vol, ROUND(100.0 * SUM(registrations) / SUM(SUM(registrations)) OVER (PARTITION BY year), 2) AS market_share_pct, DENSE_RANK() OVER (PARTITION BY year ORDER BY SUM(registrations) DESC) AS oem_rank FROM pending.fact_ev_registrations GROUP BY year, manufacturer',
    'Requires OEM-level verified registration breakdown'

UNION ALL
SELECT
    'hhi',
    'PENDING VERIFIED VAHAN DATA',
    'WITH shares AS (SELECT year, manufacturer, 100.0 * SUM(registrations) / SUM(SUM(registrations)) OVER (PARTITION BY year) AS share_pct FROM pending.fact_ev_registrations GROUP BY year, manufacturer) SELECT year, ROUND(SUM(POW(share_pct, 2)), 2) AS market_hhi FROM shares GROUP BY year',
    'Requires full OEM registration distribution for market concentration'

UNION ALL
SELECT
    'state_ranking',
    'PENDING VERIFIED VAHAN DATA',
    'SELECT year, state, SUM(registrations) AS state_vol, DENSE_RANK() OVER (PARTITION BY year ORDER BY SUM(registrations) DESC) AS state_rank, ROUND(100.0 * SUM(registrations) / SUM(SUM(registrations)) OVER (PARTITION BY year), 2) AS state_share_pct FROM pending.fact_ev_registrations GROUP BY year, state',
    'Requires state-level verified registration aggregates';
