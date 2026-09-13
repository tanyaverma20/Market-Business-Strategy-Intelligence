# Final KPI Registry: Indian Electric 2-Wheeler Market Intelligence

## 1. Overview & Classification System

This registry defines and tracks all performance indicators across the repository. To preserve data integrity, KPIs are formally segregated into three distinct operational classifications:

1. **VERIFIED KPIs (Genuinely Calculated)**: Evaluated directly from verified primary OEM catalog data. Fully populated in Python, DuckDB SQL, Power BI DAX, and Excel.
2. **SCENARIO KPIs (Simulated / Analytical Models)**: Calculated based on explicitly disclosed engineering, cost, and policy assumptions (e.g., cell prices, contribution margins).
3. **PENDING KPIs (Fail-Closed Templates)**: Market registration, growth velocity, and state volume metrics that require official multi-year Vahan exports before being activated.

---

## 2. Verified KPIs (Genuinely Calculated — 24 Metrics)

| KPI Name | Operational Definition & Formula | Implementation Layer | Source Table & Column | Verification Status | Power BI DAX Measure | Business Interpretation |
| :--- | :--- | :---: | :--- | :---: | :--- | :--- |
| **1. Total Products** | `COUNT(DISTINCT model_name)` | Python, SQL, DAX, Excel | `stg_verified_products[model_name]` | **VERIFIED** | `[Total Products]` | Breadth of commercial choices in the market (42 models). |
| **2. Total Manufacturers** | `COUNT(DISTINCT manufacturer)` | Python, SQL, DAX, Excel | `stg_verified_products[manufacturer]` | **VERIFIED** | `[Total Manufacturers]` | Verified competing automotive OEMs (11 OEMs). |
| **3. Priced Products Count** | `COUNT(ex_showroom_price_inr)` | Python, SQL, DAX, Excel | `stg_verified_products[price]` | **VERIFIED** | `[Priced Products Count]` | Models with official ex-showroom pricing captured (34 models). |
| **4. Average Product Price** | `AVG(ex_showroom_price_inr)` | Python, SQL, DAX, Excel | `stg_verified_products[price]` | **VERIFIED** | `[Average Product Price]` | Catalog benchmark mean ex-showroom price. |
| **5. Median Product Price** | `MEDIAN(ex_showroom_price_inr)` | Python, SQL, DAX, Excel | `stg_verified_products[price]` | **VERIFIED** | `[Median Product Price]` | 50th percentile price point showing price centering. |
| **6. Minimum Product Price** | `MIN(ex_showroom_price_inr)` | Python, SQL, DAX, Excel | `stg_verified_products[price]` | **VERIFIED** | `[Minimum Product Price]` | Market floor price (₹74,990 — Kinetic Green E-Luna). |
| **7. Maximum Product Price** | `MAX(ex_showroom_price_inr)` | Python, SQL, DAX, Excel | `stg_verified_products[price]` | **VERIFIED** | `[Maximum Product Price]` | Market ceiling price (₹399,000 — Ultraviolette F77 Recon). |
| **8. Price Spread** | `MAX(price) - MIN(price)` | Python, SQL, DAX, Excel | `stg_verified_products[price]` | **VERIFIED** | `[Price Spread INR]` | Full price band span across the verified EV market. |
| **9. Average Battery Capacity** | `AVG(battery_capacity_kwh)` | Python, SQL, DAX, Excel | `stg_verified_products[battery_kwh]` | **VERIFIED** | `[Average Battery Capacity]` | Mean physical battery pack capacity across models (kWh). |
| **10. Average Certified Range** | `AVG(range_km)` | Python, SQL, DAX, Excel | `stg_verified_products[range_km]` | **VERIFIED** | `[Average Certified Range]` | Mean IDC/ARAI certified range per full charge (km). |
| **11. Average Top Speed** | `AVG(top_speed_kmh)` | Python, SQL, DAX, Excel | `stg_verified_products[top_speed_kmh]` | **VERIFIED** | `[Average Top Speed]` | Maximum vehicle velocity benchmark (km/h). |
| **12. Average Motor Power** | `AVG(motor_peak_power_kw)` | Python, SQL, DAX, Excel | `stg_verified_products[motor_power_kw]` | **VERIFIED** | `[Average Motor Power]` | Mean peak powertrain output rating (kW). |
| **13. Average Price per KM** | `AVG(price / range_km)` | Python, SQL, DAX, Excel | `fact_product_metrics[price_per_km]` | **VERIFIED** | `[Average Price per KM]` | Core range cost efficiency benchmark (₹/km). |
| **14. Average Price per KWh** | `AVG(price / battery_kwh)` | Python, SQL, DAX, Excel | `fact_product_metrics[price_per_kwh]` | **VERIFIED** | `[Average Price per KWh]` | Battery capital cost efficiency benchmark (₹/kWh). |
| **15. Fleet Energy Efficiency** | `(SUM(battery_kwh)*1000) / SUM(range)` | Python, SQL, DAX, Excel | `fact_product_metrics` | **VERIFIED** | `[Weighted Fleet Energy Efficiency]` | Average energy consumption rate in Wh/km. |
| **16. Product Portfolio HHI** | `SUM(POW(mfg_share_pct, 2))` | Python, SQL, DAX, Excel | `dim_manufacturer` | **VERIFIED** | `[Product Portfolio HHI]` | Herfindahl Index of product catalog offering breadth — **1,326.53** (verified: 42 models, 11 OEMs, each share = model_count/42 × 100). |
| **17. Budget Model Count** | `COUNT(price < 100000)` | Python, SQL, DAX, Excel | `mart_product_positioning` | **VERIFIED** | `[Budget Product Count]` | Count of models in the sub-₹100k entry tier. |
| **18. Mid-Market Model Count** | `COUNT(price BETWEEN 100k AND 180k)` | Python, SQL, DAX, Excel | `mart_product_positioning` | **VERIFIED** | `[Mid-Market Product Count]` | Count of models in the core ₹100k–₹180k adoption tier. |
| **19. Premium Model Count** | `COUNT(price > 180000)` | Python, SQL, DAX, Excel | `mart_product_positioning` | **VERIFIED** | `[Premium Product Count]` | Count of models in the performance/flagship tier. |
| **20. Short-Range Model Count** | `COUNT(range < 120)` | Python, SQL, DAX, Excel | `mart_product_positioning` | **VERIFIED** | `[Short-Range Product Count]` | Count of models with < 120 km certified range. |
| **21. Standard-Range Count** | `COUNT(range BETWEEN 120 AND 180)` | Python, SQL, DAX, Excel | `mart_product_positioning` | **VERIFIED** | `[Standard-Range Product Count]` | Count of models with 120–180 km certified range. |
| **22. Long-Range Model Count** | `COUNT(range > 180)` | Python, SQL, DAX, Excel | `mart_product_positioning` | **VERIFIED** | `[Long-Range Product Count]` | Count of models with > 180 km certified range. |
| **23. High-Performance Count** | `COUNT(top_speed > 90)` | Python, SQL, DAX, Excel | `mart_product_positioning` | **VERIFIED** | `[High-Performance Product Count]` | Count of models exceeding 90 km/h top speed. |
| **24. Relative Price Position** | `CASE WHEN price < avg THEN ...` | Python, SQL, DAX, Excel | `mart_pricing_analysis` | **VERIFIED** | `[Products Below Market Average]` | Distribution of products above/below market benchmark. |

---

## 3. Scenario-Based Model KPIs (4 Metrics)

| KPI Name | Operational Definition & Formula | Implementation Layer | Disclosed Assumptions | Verification Status | Power BI DAX Measure |
| :--- | :--- | :---: | :--- | :---: | :--- |
| **Gross Margin %** | `(ASP - BOM_Cost) / ASP` | Python (`unit_economics.py`) | Cell price $115/kWh, pack ratio 1.35x, motor cost ₹12k, frame ₹20k | **SCENARIO** | Model Scenario |
| **Contribution Margin %** | `(ASP - Variable_Costs) / ASP` | Python (`unit_economics.py`) | Freight ₹3.5k, warranty ₹2.5k, dealer margin 8% | **SCENARIO** | Model Scenario |
| **Break-Even Volume** | `Fixed_Overhead / Contribution_Per_Unit` | Python (`unit_economics.py`) | Annual fixed overhead ₹45 Cr across manufacturing & SG&A | **SCENARIO** | Model Scenario |
| **Geographic Attractiveness** | `GAI = 0.3*Vol + 0.25*Inc + 0.2*Dens + 0.15*Pol + 0.1*Urb` | Python (`geographic_analysis.py`) | Weights derived from multi-criteria strategic decision matrix | **SCENARIO** | Model Scenario |

---

## 4. Pending Market Registration KPIs (Fail-Closed — 8 Metrics)

| KPI Name | Required Authoritative Source | Planned Formula | Current Status | Safeguard Enforcement |
| :--- | :--- | :--- | :---: | :--- |
| **Total EV Registrations** | Official MoRTH Vahan 4.0 export | `SUM(registrations)` | **PENDING** | Table empty (0 rows); DAX returns `BLANK()`. |
| **YoY Market Growth %** | Multi-year consecutive Vahan series | `(Vol_t - Vol_{t-1}) / Vol_{t-1}` | **PENDING** | Table empty (0 rows); DAX returns `BLANK()`. |
| **Market CAGR %** | Multi-year consecutive Vahan series | `(Vol_end / Vol_start)^(1/n) - 1` | **PENDING** | Table empty (0 rows); DAX returns `BLANK()`. |
| **EV Penetration %** | Total 2W and EV Vahan categories | `EV_Registrations / Total_2W_Registrations` | **PENDING** | Table empty (0 rows); DAX returns `BLANK()`. |
| **OEM Market Share %** | Maker-wise Vahan registration export | `OEM_Registrations / Total_EV_Registrations` | **PENDING** | Table empty (0 rows); DAX returns `BLANK()`. |
| **Market Volume HHI** | Full OEM registration distribution | `SUM(POW(OEM_Share, 2))` | **PENDING** | Table empty (0 rows); DAX returns `BLANK()`. |
| **State Registration Rank** | State-wise Vahan registration totals | `RANK() OVER (ORDER BY State_Vol DESC)` | **PENDING** | Table empty (0 rows); DAX returns `BLANK()`. |
| **Market Intelligence Status** | Provenance verification flag | Literal string | **PENDING** | Returns `"PENDING VERIFIED VAHAN DATA"`. |
