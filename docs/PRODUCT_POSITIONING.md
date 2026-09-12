# Product Positioning

## Scope

This section documents the verified-only positioning framework for the product catalog. It is designed to classify products based on price, range, battery, and performance without creating strategic conclusions that are unsupported by the available data.

## Methodology

Products are classified using configurable thresholds for:

- Price bucket: budget, mid-market, premium
- Range bucket: short-range, mainstream-range, long-range
- Battery bucket: compact-battery, standard-battery, high-battery
- Performance bucket: entry, balanced, high-performance

The classification logic is implemented in [src/analytics/positioning_analysis.py](src/analytics/positioning_analysis.py). The output file [data/processed/product_positioning.csv](data/processed/product_positioning.csv) records an analytical summary for each product with the segment assignment and the data-driven reasoning that supports it.

## Why this matters

A business strategist can use this to understand how the verified catalog is distributed across price and capability bands, and to identify where products cluster or where there is a potential whitespace area, such as budget-long-range or value-high-battery. The output is descriptive and analytical, not a recommendation.

## Data limitations

- Coverage is limited to the verified product catalog only.
- No market-share, retailer, or channel data is used to infer positioning.
- Product segments are derived from the observed catalog, not from an external benchmark or strategic claim.
- Whitespace labels are only presented when the underlying verified product fields are present.

## Output fields

- manufacturer
- product
- model_name
- price_vs_range
- price_vs_battery
- price_vs_performance
- whitespace_areas
- segment_summary
- reasoning
- metric_type
- methodology_version

## Verification status

The framework is derived from verified product inputs and is therefore valid for catalog-level competitive analysis. It does not claim to represent market opportunity or strategic recommendation.
