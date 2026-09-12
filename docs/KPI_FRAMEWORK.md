# KPI Framework

## Scope and status rules

This framework is intentionally fail-closed. A KPI is only counted as implemented when it is calculated from verified source data or explicitly marked as a reusable template with a pending status. No market, state, or cost KPI is treated as factual when the underlying data is missing.

Statuses used throughout this project:

- VERIFIED: calculated from verified catalog data
- DERIVED FROM VERIFIED: mathematically derived from verified inputs
- PENDING VERIFIED DATA: required market or state dataset is not yet available
- PENDING VERIFIED COST DATA: cost/BOM data is not yet available
- PROXY / NOT ALLOWED: excluded from factual analytics

## A. Currently calculable from verified data

| KPI | Business definition | Formula | Unit | Required inputs | Source dataset | Verification status | Calculation status | Interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Manufacturer count | Number of distinct manufacturers in the verified catalog | nunique(manufacturer) | count | manufacturer | verified_product_catalog_2025_2026.csv | VERIFIED | VERIFIED | Measures breadth of verified supplier coverage. |
| Product count | Number of distinct product variants in the verified catalog | nunique(model_name) | count | model_name | verified_product_catalog_2025_2026.csv | VERIFIED | VERIFIED | Measures catalog breadth and competitive density. |
| Average product price | Mean verified ex-showroom price | mean(ex_showroom_price_inr) | INR | ex_showroom_price_inr | verified_product_catalog_2025_2026.csv | VERIFIED | DERIVED FROM VERIFIED | Shows the typical observed price level. |
| Median product price | Median verified ex-showroom price | median(ex_showroom_price_inr) | INR | ex_showroom_price_inr | verified_product_catalog_2025_2026.csv | VERIFIED | DERIVED FROM VERIFIED | Useful for avoiding skew from premium outliers. |
| Price per certified km | Price relative to certified range | ex_showroom_price_inr / certified_range_km | INR/km | ex_showroom_price_inr, certified_range_km | verified_product_catalog_2025_2026.csv | VERIFIED | DERIVED FROM VERIFIED | Lower values indicate better value-per-range for the same catalog. |
| Price per kWh | Price relative to battery size | ex_showroom_price_inr / battery_capacity_kwh | INR/kWh | ex_showroom_price_inr, battery_capacity_kwh | verified_product_catalog_2025_2026.csv | VERIFIED | DERIVED FROM VERIFIED | Lower values indicate better battery-cost efficiency. |
| Average battery capacity | Mean verified battery size | mean(battery_capacity_kwh) | kWh | battery_capacity_kwh | verified_product_catalog_2025_2026.csv | VERIFIED | DERIVED FROM VERIFIED | Helps describe the typical energy capacity in the catalog. |
| Average certified range | Mean certified range | mean(certified_range_km) | km | certified_range_km | verified_product_catalog_2025_2026.csv | VERIFIED | DERIVED FROM VERIFIED | Shows average range capability in the catalog. |
| Average top speed | Mean verified top speed | mean(top_speed_kmh) | km/h | top_speed_kmh | verified_product_catalog_2025_2026.csv | VERIFIED | DERIVED FROM VERIFIED | Describes performance envelope across the product set. |
| Average motor power | Mean verified peak motor power | mean(motor_peak_power_kw) | kW | motor_peak_power_kw | verified_product_catalog_2025_2026.csv | VERIFIED | DERIVED FROM VERIFIED | Helps relate product performance to hardware capability. |
| Range realization % | Real-world vs certified range | real_world_range_km / certified_range_km * 100 | % | real_world_range_km, certified_range_km | verified_product_catalog_2025_2026.csv | VERIFIED | DERIVED FROM VERIFIED | Measures how well real-world experience matches official range claims. |
| Product value score | Weighted normalized value score | configured weighted sum of normalized range, battery, price efficiency, and performance | 0-100 | ex_showroom_price_inr, certified_range_km, battery_capacity_kwh, top_speed_kmh | verified_product_catalog_2025_2026.csv | VERIFIED | DERIVED FROM VERIFIED | Ranks product value in a catalog-relative way. |
| Competitive intensity score | Relative competition density for the verified catalog | manufacturer count, product count, and price spread mix | 0-100 | manufacturer, model_name, ex_showroom_price_inr | verified_product_catalog_2025_2026.csv | VERIFIED | DERIVED FROM VERIFIED | Shows whether the verified category is concentrated or fragmented. |

## B. Pending verified market data

| KPI | Business definition | Formula | Unit | Required inputs | Source dataset | Verification status | Calculation status | Interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Annual EV registrations | Total EV sales by year | sum(e2w_registrations) by year | units | year, e2w_registrations | verified market registration dataset | PENDING VERIFIED DATA | PENDING VERIFIED DATA | Requires official market-registration data. |
| Monthly EV registrations | Monthly EV volume pattern | sum(e2w_registrations) by date | units | date, e2w_registrations | verified market registration dataset | PENDING VERIFIED DATA | PENDING VERIFIED DATA | Seasonal analysis must wait for validated market data. |
| YoY growth | Annual change relative to previous year | ((current - previous) / previous) * 100 | % | year, e2w_registrations | verified market registration dataset | PENDING VERIFIED DATA | PENDING VERIFIED DATA | Measures growth only when official annual data exists. |
| CAGR | Compound annual growth rate | ((end / start)^(1 / years) - 1) * 100 | % | year, e2w_registrations | verified market registration dataset | PENDING VERIFIED DATA | PENDING VERIFIED DATA | Requires multi-year verified registration history. |
| EV penetration | EV share of total 2W registrations | (e2w_registrations / total_2w_registrations) * 100 | % | e2w_registrations, total_2w_registrations | verified market registration dataset | PENDING VERIFIED DATA | PENDING VERIFIED DATA | No factual share can be reported without official totals. |
| TAM | Total addressable market | configurable market-size model | units or INR | total_market_units | verified market sizing inputs | PENDING VERIFIED DATA | PENDING VERIFIED DATA | Model framework only; no business number without verified assumptions. |
| SAM | Serviceable market | target_units * target_share | units or INR | target_units, target_share | verified market sizing inputs | PENDING VERIFIED DATA | PENDING VERIFIED DATA | Framework placeholder only. |
| SOM | Serviceable obtainable market | SAM * target_market_share | units or INR | sam_units, target_market_share | verified market sizing inputs | PENDING VERIFIED DATA | PENDING VERIFIED DATA | Framework placeholder only. |
| OEM market share | Share of annual EV registrations by OEM | (OEM registrations / total registrations) * 100 | % | oem_name, year, e2w_registrations | verified OEM registration dataset | PENDING VERIFIED DATA | PENDING VERIFIED DATA | Not calculated because current OEM market data is not verified. |
| HHI | Market concentration | sum(market_share_pct^2) | index | oem_name, year, market_share_pct | verified OEM registration dataset | PENDING VERIFIED DATA | PENDING VERIFIED DATA | HHI remains blocked until market-share dataset is validated. |

## C. Pending verified state data

| KPI | Business definition | Formula | Unit | Required inputs | Source dataset | Verification status | Calculation status | Interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Geographic Attractiveness Index (GAI) | State-level attractiveness | weighted normalized component score | 0-100 | state, market_size, ev_penetration, growth, purchasing_power, charging_infrastructure, policy_score | verified state indicator dataset | PENDING VERIFIED DATA | PENDING VERIFIED DATA | The scoring template is complete, but actual rankings remain blocked because state indicators are not verified. |

## D. Pending verified cost data

| KPI | Business definition | Formula | Unit | Required inputs | Source dataset | Verification status | Calculation status | Interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Gross margin % | Margin relative to selling price | (selling_price - cogs) / selling_price * 100 | % | selling_price, cogs | verified cost input template | PENDING VERIFIED COST DATA | PENDING VERIFIED COST DATA | Requires a verified BOM/cost basis. |
| Contribution margin | Revenue contribution after variable costs | selling_price * units_sold - variable_cost * units_sold | INR | selling_price, variable_cost, units_sold | verified cost input template | PENDING VERIFIED COST DATA | PENDING VERIFIED COST DATA | Cannot be reported without operational cost inputs. |
| Contribution margin % | Contribution as a percentage of selling price | ((selling_price - variable_cost) / selling_price) * 100 | % | selling_price, variable_cost | verified cost input template | PENDING VERIFIED COST DATA | PENDING VERIFIED COST DATA | Requires verified variable-cost assumptions. |
| Break-even units | Units required to cover fixed costs | fixed_cost / contribution_margin_per_unit | units | fixed_cost, selling_price, variable_cost | verified cost input template | PENDING VERIFIED COST DATA | PENDING VERIFIED COST DATA | Requires verified fixed and variable cost inputs. |
| Break-even revenue | Revenue needed to break even | break_even_units * selling_price | INR | fixed_cost, selling_price, variable_cost | verified cost input template | PENDING VERIFIED COST DATA | PENDING VERIFIED COST DATA | Formula is implemented; no factual values without cost data. |
| TCO | Total cost of ownership | purchase_price - subsidy + electricity + maintenance + insurance + financing + other costs | INR | purchase_price, subsidy, electricity_cost, maintenance_cost, insurance_cost | verified cost and ownership assumptions | PENDING VERIFIED COST DATA | PENDING VERIFIED COST DATA | Framework implemented; no actual TCO claims until verified cost inputs exist. |

## Interpretation guidance

- Use product-level KPIs for competitive benchmarking within the verified catalog.
- Treat all market, state, and cost KPIs as planning frameworks until their underlying source is verified.
- Keep unsupported metrics clearly labeled as pending, not as factual outputs.
