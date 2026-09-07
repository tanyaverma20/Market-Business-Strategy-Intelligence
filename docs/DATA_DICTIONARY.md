# Project Data Dictionary

> **Project**: Market & Business Strategy Intelligence — Indian Electric 2-Wheeler (e2W) Strategy  
> **Document Type**: Technical Data Dictionary (Phase 1 Deliverable)  
> **Coverage**: Raw & Processed Datasets in `data/raw/` and `data/processed/`

---

## 1. Monthly Vahan Registrations Dataset (`processed_vahan_monthly.csv`)

| Variable Name | Data Type | Unit | Description | Classification | Validation Rules / Range | Source Mapping |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `year` | Integer | YYYY | Calendar Year of registration | [OBSERVED] | 2020 <= `year` <= 2025 | Vahan 4.0 Dashboard |
| `month` | Integer | MM | Month of registration | [OBSERVED] | 1 <= `month` <= 12 | Vahan 4.0 Dashboard |
| `year_month` | String | YYYY-MM | ISO Year-Month indicator | [OBSERVED] | Regex `^\d{4}-\d{2}$` | Vahan 4.0 Dashboard |
| `date` | Date | YYYY-MM-DD | First day of registration month | [CALCULATED] | Valid Date | Derived from `year_month` |
| `state` | String | Text | Full Indian State or UT Name | [OBSERVED] | Non-null, 28 States + UTs | Vahan 4.0 Dashboard |
| `state_code` | String | Code | Two-letter ISO State Code | [OBSERVED] | 2-letter uppercase | Vahan 4.0 Dashboard |
| `e2w_registrations` | Integer | Units | Count of registered High-Speed e2Ws | [OBSERVED] | `>= 0` | Vahan 4.0 Dashboard |
| `total_2w_registrations` | Integer | Units | Count of total registered 2Ws (ICE + EV) | [DERIVED ESTIMATE] | `>= e2w_registrations` | Vahan / SIAM Proxy |
| `ev_penetration_pct` | Float | % | e2W Share of total 2W registrations | [CALCULATED] | `0.0 <= x <= 100.0` | `(e2w_registrations / total_2w) * 100` |
| `data_source` | String | Text | Reference provenance | [METADATA] | Non-null string | Vahan 4.0 Gazette |

---

## 2. OEM Market Share Dataset (`processed_oem_market_shares.csv` & `processed_market_hhi.csv`)

| Variable Name | Data Type | Unit | Description | Classification | Validation Rules / Range | Source Mapping |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `year` | Integer | YYYY | Calendar Year | [OBSERVED] | 2020 <= `year` <= 2025 | Vahan / MHI |
| `oem_name` | String | Text | Manufacturer / Brand Name | [OBSERVED] | Non-null string | Vahan / SEBI Filings |
| `oem_category` | String | Category | Classification (Pure-Play Startup, Legacy OEM, Regional) | [DERIVED ESTIMATE] | Enum: Startup, Legacy, Regional | Strategic Classification |
| `e2w_registrations` | Integer | Units | Total annual e2W registrations by OEM | [OBSERVED] | `>= 0` | Vahan / MHI Releases |
| `market_share_pct` | Float | % | Percentage share of total annual national e2W sales | [CALCULATED] | `0.0 <= x <= 100.0` | `(oem_reg / total_annual_reg) * 100` |
| `hhi_index` | Float | Index | Herfindahl-Hirschman Index of market concentration | [CALCULATED] | `0 <= HHI <= 10,000` | `Sum(market_share_pct ^ 2)` |

---

## 3. Competitor Product Catalog (`processed_competitor_specs.csv`)

| Variable Name | Data Type | Unit | Description | Classification | Validation Rules / Range | Source Mapping |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `manufacturer` | String | Text | OEM Brand Name | [OBSERVED] | Non-null | Official Brand Portfolios |
| `model_name` | String | Text | Model Variant Name | [OBSERVED] | Non-null | Official Brand Portfolios |
| `product_category` | String | Text | Target segment (Budget Commuter, Mid-Market, Premium, etc.) | [DERIVED ESTIMATE] | Standardized Tiers | Strategic Classification |
| `ex_showroom_price_inr` | Float | INR (₹) | Official ex-showroom price | [OBSERVED] | `30,000 <= x <= 3,000,000` | OEM Published Price List |
| `battery_capacity_kwh` | Float | kWh | Installed usable battery capacity | [OBSERVED] | `1.0 <= x <= 10.0` | Technical Datasheet |
| `battery_chemistry` | String | Text | Cell Chemistry type (LFP vs NMC) | [OBSERVED] | Enum: LFP, NMC | Technical Datasheet / DRHP |
| `certified_idc_range_km` | Float | km | Indian Driving Cycle (IDC) range | [OBSERVED] | `50 <= x <= 300` | ARAI / ICAT Certificate |
| `real_world_range_km` | Float | km | Tested real-world range under normal riding | [OBSERVED] | `30 <= x <= 250` | OEM Technical Specs |
| `top_speed_kmh` | Float | km/h | Top speed capability | [OBSERVED] | `40 <= x <= 150` | Technical Datasheet |
| `motor_peak_power_kw` | Float | kW | Peak electric motor output | [OBSERVED] | `1.5 <= x <= 15.0` | Technical Datasheet |
| `charging_time_hours_0_80`| Float | Hours | Standard home charging time (0-80%) | [OBSERVED] | `1.0 <= x <= 12.0` | Technical Datasheet |
| `price_to_real_range_ratio`| Float | ₹ / km | Ex-showroom price per real-world range km | [CALCULATED] | `price / real_world_range_km` | Calculated Metric |
| `price_to_battery_kwh_ratio`| Float | ₹ / kWh | Ex-showroom price per kWh capacity | [CALCULATED] | `price / battery_capacity_kwh` | Calculated Metric |
| `pm_edrive_subsidy_fy25_inr`| Float | INR (₹) | Applicable PM E-DRIVE subsidy (FY25) | [CALCULATED] | `Min(kWh * 5000, 10000)` | PM E-DRIVE Policy Rules |
| `effective_price_post_subsidy_fy25_inr`| Float | INR (₹) | Post-subsidy net price | [CALCULATED] | `price - subsidy` | Calculated Metric |

---

## 4. State Socioeconomic Indicators (`processed_state_indicators.csv`)

| Variable Name | Data Type | Unit | Description | Classification | Validation Rules / Range | Source Mapping |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `state` | String | Text | Full State / UT Name | [OBSERVED] | Non-null | MoSPI / RBI |
| `state_code` | String | Code | Two-letter ISO State Code | [OBSERVED] | 2-letter uppercase | Standard ISO |
| `population_2024_est_millions` | Float | Millions | Estimated state population (2024) | [OBSERVED] | `0.5 <= x <= 300.0` | MoSPI Census Projections |
| `urbanization_pct` | Float | % | Percentage of urban population | [OBSERVED] | `10.0 <= x <= 100.0` | MoSPI Statistics |
| `per_capita_nsdp_inr` | Float | INR (₹) | Per Capita Net State Domestic Product | [OBSERVED] | `40,000 <= x <= 1,000,000` | RBI Handbook 2024 |
| `public_charging_stations_count` | Integer | Units | Count of operational public EV charging stations | [OBSERVED] | `>= 0` | BEE EV Yatra Portal |
| `charging_stations_per_million_pop` | Float | Density | Charging stations per million residents | [CALCULATED] | `>= 0` | `stations / pop_millions` |
| `state_ev_policy_active` | String | Yes/No | Whether dedicated state EV policy is active | [OBSERVED] | Enum: Yes, No | NITI Aayog e-AMRIT |
| `road_tax_exemption_pct` | Float | % | Road tax exemption percentage for e2W | [OBSERVED] | `0 <= x <= 100` | State EV Policy Gazettes |
| `subsidy_capital_support_score` | Float | Score | Composite score of state incentive support (0-100) | [DERIVED ESTIMATE] | `0 <= x <= 100` | NITI Aayog Policy Scorecard |

---

## 5. Policy Timeline Dataset (`processed_policy_timeline.csv`)

| Variable Name | Data Type | Unit | Description | Classification | Source Mapping |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `policy_scheme` | String | Text | Official name of government incentive scheme | [OBSERVED] | MHI Gazette Notifications |
| `start_date` | Date | YYYY-MM-DD | Effective start date | [OBSERVED] | MHI Gazette Notifications |
| `end_date` | Date | YYYY-MM-DD | Scheme expiration date | [OBSERVED] | MHI Gazette Notifications |
| `incentive_rate_per_kwh_inr` | Float | ₹ / kWh | Subsidy payout rate per kWh battery pack | [OBSERVED] | MHI Gazette Notifications |
| `max_cap_per_vehicle_inr` | Float | INR (₹) | Maximum subsidy cap per vehicle | [OBSERVED] | MHI Gazette Notifications |
| `total_budget_outlay_cr` | Float | INR Cr | Total scheme financial outlay | [OBSERVED] | MHI Gazette Notifications |
| `key_objectives` | String | Text | Official policy objectives and rules | [OBSERVED] | MHI Gazette Notifications |

---

> **Document Status**: Complete Data Dictionary verified for all 5 Phase 1 datasets.
