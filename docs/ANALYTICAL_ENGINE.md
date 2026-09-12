# Analytical Engine

## Purpose

This analytical engine is intentionally limited to verified, source-linked data. It supports product-level competitive analytics and pricing/positioning frameworks, while keeping market, state, and unit-economics calculations in a safe pending state until verified datasets are available.

The engine is designed to avoid fabricated market-registration outputs and to prevent mixing verified and unverified sources in the same analytical result.

## Architecture

The Python implementation is organized under `src/analytics` with a small set of modular files:

- `market_analysis.py`: reusable market functions and verified-data gating
- `competitive_analysis.py`: verified product and portfolio metrics
- `pricing_analysis.py`: price, value, and percentile metrics
- `positioning_analysis.py`: competitive positioning and whitespace framework
- `unit_economics.py`: cost model schema and sensitivity structure
- `geographic_analysis.py`: GAI scoring template and weight configuration
- `kpi_engine.py`: KPI registry and status engine

The root processing pipeline remains in `src/data_processing.py`, which validates provenance, schema, and raw dataset integrity before writing processed outputs.

## Verified vs pending analytics

Only one source is currently eligible as observed analytics:

- `data/raw/verified_product_catalog_2025_2026.csv`
- `data/processed/processed_verified_product_catalog.csv`

This dataset is subject to source-linked verification checks and is therefore used for:

- manufacturer count
- product count
- category distribution
- price comparison
- battery/range/performance comparison
- price efficiency metrics
- product positioning
- pricing value score

The following are intentionally pending because the project does not currently contain verified, official market data:

- monthly EV registrations
- annual EV registrations
- YoY growth
- CAGR
- EV penetration
- TAM/SAM/SOM
- OEM market share
- HHI
- state-level market analysis
- GAI rankings
- profitability and break-even calculations without cost inputs
- strategic priority scoring that depends on verified state and market data

## Validation and provenance rules

All analytical functions follow these rules:

1. Accept data as input and return a DataFrame or structured result.
2. Validate required columns before computing.
3. Fail on invalid numerical values when the metric is impossible.
4. Return a `PENDING VERIFIED DATA` or `VERIFIED DATA REQUIRED` status when the required source is unavailable.
5. Never fill missing values with guesses.
6. Preserve provenance class labels and validation output from the processing pipeline.

## Core formulas

### Competitive value score

The default value score uses configurable weights:

- range: 0.40
- battery: 0.20
- price efficiency: 0.25
- performance: 0.15

The formula is normalized across the product set and applied as a weighted score, without claiming that the weights are universal truths. They are default assumptions and can be changed in the configuration section of the module.

### Price per km

`price_per_km = ex_showroom_price_inr / certified_range_km`

### Price per kWh

`price_per_kwh = ex_showroom_price_inr / battery_capacity_kwh`

### Range realization

`range_realization_pct = real_world_range_km / certified_range_km * 100`

Only calculated when both ranges are available and the certified range is greater than zero.

### GAI

`GAI = sum(weight_i * normalized_indicator_i)`

The current implementation does not produce a factual ranking because the state-indicator dataset is unverified and proxy-based.

## Inputs and outputs

### Required verified inputs

For product analytics, the engine expects columns such as:

- manufacturer
- model_name
- vehicle_category
- ex_showroom_price_inr
- battery_capacity_kwh
- certified_range_km
- real_world_range_km
- top_speed_kmh
- motor_peak_power_kw
- verification_status

### Generated outputs

The pipeline can produce these analytical results in `data/processed` and `outputs`:

- competitive_product_metrics.csv
- competitive_manufacturer_summary.csv
- pricing_metrics.csv
- product_positioning.csv
- kpi_registry.csv
- kpi_status.csv
- unit_economics_template.csv
- geographic_scoring_template.csv

## How to run

From the repository root:

```bash
python src/data_processing.py
python -m pytest -q
```

The processing step writes validation results to `data/processed/validation_results.json` and writes the processed product dataset and other provenance-tagged files under `data/processed`.

## Assumptions

- Verified product catalog entries are the only currently accepted observed data source.
- Market-state registrations remain pending until official, verified datasets are supplied.
- Cost models are kept as templates until BOM, manufacturing, distribution, and warranty data are verified.
- The engine is designed to support future dataset ingestion without retroactively changing past results.

## Current status

The engine is active for verified product analytics and ready to support future verified market/state analytics once those official datasets are added.
