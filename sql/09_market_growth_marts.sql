-- 09_market_growth_marts.sql
-- SEBI-Verified market growth analytics (FY2021-FY2024)
-- Source: Ola Electric Mobility Limited RHP (August 2024) - SEBI statutory filing
-- GOVERNANCE: Industry totals from public audited statutory document.
-- State-level breakdown NOT available from this source - state ranking remains fail-closed.

CREATE SCHEMA IF NOT EXISTS mart;

DROP TABLE IF EXISTS mart.sebi_market_growth;
DROP TABLE IF EXISTS mart.tam_sam_som;
DROP VIEW IF EXISTS mart.market_growth_summary;

CREATE TABLE mart.sebi_market_growth (
    fiscal_year VARCHAR PRIMARY KEY,
    calendar_year_end INTEGER,
    industry_e2w_units BIGINT,
    yoy_growth_pct DOUBLE,
    cagr_fy2021_fy2024_pct DOUBLE,
    data_classification VARCHAR,
    source VARCHAR,
    provenance_status VARCHAR,
    coverage_note VARCHAR
);

INSERT INTO mart.sebi_market_growth VALUES
('FY2021',2021,41000,NULL,NULL,'OBSERVED - SEBI RHP 2024','Ola Electric RHP Aug 2024 - SEBI statutory','verified_primary_source','National India e2W total; state-level not available'),
('FY2022',2022,249000,507.3,NULL,'OBSERVED - SEBI RHP 2024','Ola Electric RHP Aug 2024 - SEBI statutory','verified_primary_source','National India e2W total; state-level not available'),
('FY2023',2023,728000,192.4,NULL,'OBSERVED - SEBI RHP 2024','Ola Electric RHP Aug 2024 - SEBI statutory','verified_primary_source','National India e2W total; state-level not available'),
('FY2024',2024,944000,29.7,NULL,'OBSERVED - SEBI RHP 2024','Ola Electric RHP Aug 2024 - SEBI statutory','verified_primary_source','National India e2W total; state-level not available');

UPDATE mart.sebi_market_growth
SET cagr_fy2021_fy2024_pct = ROUND(
    100.0 * (POWER(
        (SELECT industry_e2w_units::DOUBLE FROM mart.sebi_market_growth WHERE fiscal_year='FY2024') /
        NULLIF((SELECT industry_e2w_units::DOUBLE FROM mart.sebi_market_growth WHERE fiscal_year='FY2021'),0),
        1.0/3) - 1.0), 1);

CREATE TABLE mart.tam_sam_som (
    scenario VARCHAR PRIMARY KEY,
    description VARCHAR,
    verified_fy2024_industry_units BIGINT,
    verified_source VARCHAR,
    fy2025_growth_assumption_pct DOUBLE,
    tam_units BIGINT,
    tam_revenue_inr_crore DOUBLE,
    geographic_concentration_pct DOUBLE,
    segment_concentration_pct DOUBLE,
    sam_units BIGINT,
    sam_revenue_inr_crore DOUBLE,
    attainable_share_pct DOUBLE,
    som_units BIGINT,
    som_revenue_inr_crore DOUBLE,
    avg_price_per_unit_inr DOUBLE,
    data_classification_tam VARCHAR,
    data_classification_sam VARCHAR,
    data_classification_som VARCHAR,
    methodology_version VARCHAR
);

INSERT INTO mart.tam_sam_som VALUES
('Conservative Case','Slower adoption: policy delays, subsidy uncertainty',944000,
 'Ola Electric RHP Aug 2024 - SEBI statutory filing',10.0,
 1038400,1246.1,60.0,70.0,435648,522.8,1.5,6534,78.4,120000,
 'OBSERVED(FY24)+ASSUMPTION(growth)','ASSUMPTION','ASSUMPTION','v1.0-2026-09-24'),
('Base Case','Moderate growth; PM E-DRIVE scheme operational',944000,
 'Ola Electric RHP Aug 2024 - SEBI statutory filing',25.0,
 1180000,1469.1,70.0,80.0,660800,822.6,3.0,19824,246.8,124466,
 'OBSERVED(FY24)+ASSUMPTION(growth)','ASSUMPTION','ASSUMPTION','v1.0-2026-09-24'),
('Upside Case','Strong adoption: PM E-DRIVE full deployment, grid expansion',944000,
 'Ola Electric RHP Aug 2024 - SEBI statutory filing',45.0,
 1369800,1780.7,80.0,85.0,930660,1209.9,5.0,46533,604.9,130000,
 'OBSERVED(FY24)+ASSUMPTION(growth)','ASSUMPTION','ASSUMPTION','v1.0-2026-09-24');

CREATE OR REPLACE VIEW mart.market_growth_summary AS
SELECT
    fiscal_year, calendar_year_end, industry_e2w_units,
    yoy_growth_pct, cagr_fy2021_fy2024_pct,
    data_classification, provenance_status,
    'National India e2W; state-level Vahan data not available' AS state_data_status
FROM mart.sebi_market_growth
ORDER BY calendar_year_end;
