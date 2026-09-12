# SQL Analytics Layer

## Database architecture

This project uses DuckDB as the local analytical engine because it is lightweight, portable, fast, and does not require a paid database service.

Suggested warehouse layering:

RAW / SOURCE
  -> local CSV inputs under data/raw and processed CSVs under data/processed

STAGING
  -> stg_verified_products
  -> treated as a cleaned, provenance-aware intermediate layer

ANALYTICAL / MART
  -> mart_competitive_analysis
  -> mart_pricing_analysis
  -> mart_product_positioning
  -> kpi_status

PENDING MARKET
  -> pending.fact_ev_registrations
  -> intentionally empty; used as a schema placeholder only

## SQL engine and version assumptions

- Engine: DuckDB
- Version: current local installation; the scripts use standard DuckDB SQL constructs and read_csv_auto
- Assumption: the project runs on a local machine with Python and DuckDB installed via pip

## Initialization

From the project root:

python -m pip install duckdb pandas
python src/run_sql_pipeline.py

This creates a local database at:

data/processed/sql/e2w_sql.duckdb

## Tables and views

- stg_verified_products: verified catalog data with provenance metadata
- dim_manufacturer: supplier-level rollup
- dim_product: product dimension
- mart_competitive_analysis: product-level comparison and ranking
- mart_pricing_analysis: price, percentile, and value positioning
- mart_product_positioning: price, battery, range, and performance classification
- kpi_status: verified KPI output
- sql_data_quality_results: validation checks
- pending.fact_ev_registrations: fail-closed pending market schema

## Data quality checks

The SQL layer validates:

- duplicate products
- duplicate manufacturer/model combinations
- null required fields
- negative prices
- invalid battery capacities
- invalid ranges
- invalid speed values
- invalid motor power
- unverified records
- missing provenance

These are surfaced in sql_data_quality_results and are not silently ignored.

## Window functions used

The SQL layer uses meaningful business windows, including:

- ROW_NUMBER() OVER (PARTITION BY manufacturer ORDER BY ex_showroom_price_inr)
- DENSE_RANK() OVER (PARTITION BY manufacturer ORDER BY ex_showroom_price_inr)
- PERCENT_RANK() OVER (ORDER BY ex_showroom_price_inr)
- NTILE(4) OVER (ORDER BY ex_showroom_price_inr)
- SUM() OVER ()
- AVG() OVER ()

These answer questions such as:

- Which products rank highest within each manufacturer?
- Which products have the best price efficiency?
- How does each product compare against the market average price?

## Verified vs pending data

Verified dataset:

- data/processed/processed_verified_product_catalog.csv

Pending market data:

- fact_ev_registrations placeholder remains empty
- all market queries remain marked as PENDING VERIFIED VAHAN DATA

## Example SQL business questions

1. Which manufacturers have the largest verified product portfolios?
2. Which products offer the best price-per-range?
3. Which products are relatively expensive for their range?
4. Which manufacturers dominate particular product segments?
5. Which products rank highest within their manufacturer?
6. Which products represent potential competitive whitespace?
7. How does product pricing vary by manufacturer?
8. Which products provide the strongest measurable value based on the verified product scoring logic?

## SQL execution steps

1. Load the verified catalog into DuckDB.
2. Create schema objects.
3. Run validation checks.
4. Create analytics marts.
5. Export CSV outputs under data/processed/sql.
6. Review sql_data_quality_results before using any result for business reporting.

## Limitations

The SQL layer intentionally does not populate market, state, or cost analytics from proxy data. Market queries remain templates until verified Vahan and other official market inputs are supplied.
