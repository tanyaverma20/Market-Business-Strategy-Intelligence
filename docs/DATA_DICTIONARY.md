# Data Dictionary

Every processed file includes `source_dataset`, `provenance_class`, and `eligible_as_observed_analytics`. Only the verified product catalog is currently eligible as observed data, and only for product/competitor fields.

| Dataset / field | Type | Definition |
|---|---|---|
| `verified_product_catalog_2025_2026.manufacturer`, `model_name`, `vehicle_category` | text | Source-linked OEM/model identity and vehicle type. |
| `ex_showroom_price_inr`, `price_basis` | INR, text | Price exactly as cited; basis preserves location/effective-incentive/introductory qualification. Blank price is not zero. |
| `battery_capacity_kwh`, `range_km`, `range_standard`, `top_speed_kmh`, `motor_peak_power_kw` | numeric/text | Only values stated in the row's cited OEM source. `range_standard` distinguishes IDC/certified from manufacturer-described real-world range. |
| `launch_status` | text | Current or named launch status as supported by the cited source. |
| `source_url`, `source_type`, `accessed_date`, `verification_status`, `verification_notes` | text/date | Minimum evidence trail for every verified product row. |
| `price_per_certified_km_inr`, `price_per_kwh_inr` | numeric | Derived competitive metrics that divide verified price by verified range or battery. |
| `range_realization_pct` | numeric | `real_world_range_km / certified_range_km * 100`; only populated when both numbers are supported. |
| `value_score` | numeric | Configurable weighted value model using range, battery, price efficiency, and performance. |
| `gai_score`, `priority_tier` | numeric/text | Geographic attractiveness framework outputs; populated only when verified state indicators are supplied. |
| `status`, `metric_type`, `weight_configuration` | text | Analytical status flags: `observed`, `derived`, `PENDING VERIFIED DATA`, or configuration metadata. |
| `vahan_e2w_registrations_monthly.*` | mixed | Generated proxy only. `ev_penetration_pct` is derived and non-factual. |
| `oem_e2w_registrations_annual.*`, `processed_market_hhi.*` | mixed | Proxy and derived proxy outputs only. |
| `state_socioeconomic_indicators.*` | mixed | Unverified proxy state indicators. |
| `policy_incentive_timeline.*` | mixed | Unverified transcription pending official-document verification. |

The pipeline validates schemas, dates, duplicates, missing values, supplied numeric values, non-negative counts, state names/codes, and e2W counts exceeding total 2W counts. It writes checksums and provenance findings to `data/processed/validation_results.json`.
