# Power BI Centralized KPI-to-Visual Mapping Matrix

## 1. Overview

This traceability matrix maps business performance metrics across the Power BI layer. Every metric is mapped to its underlying DAX measure, physical source table/column, data verification status, intended dashboard visual, and executive business interpretation.

---

## 2. Verified Business & Product KPIs (Currently Active)

| KPI Name | DAX Measure | Source Table & Column | Verification Status | Current Availability | Intended Dashboard Visual | Business Interpretation |
| :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| **Total Products** | `[Total Products]` | `FactProductMetrics[product]` | Verified | **Available (30)** | Single Value Card (Page 1) | Breadth of commercial offerings in the verified Indian e2W market. |
| **Active OEMs** | `[Total Manufacturers]` | `DimManufacturer[manufacturer]` | Verified | **Available (5)** | Single Value Card (Page 1) | Number of primary verified automotive competitors in the catalog. |
| **Average Price** | `[Average Product Price]` | `FactProductMetrics[price]` | Verified | **Available (₹124,466)** | Card / Bar Chart (Pages 1, 2, 3) | Market arithmetic benchmark price across priced models. |
| **Median Price** | `[Median Product Price]` | `FactProductMetrics[price]` | Verified | **Available (₹126,078)** | Card / Box-Whisker (Page 3) | 50th percentile price point showing absence of significant price skew. |
| **Market Price Floor** | `[Minimum Product Price]` | `FactProductMetrics[price]` | Verified | **Available (₹84,999)** | Card / Range Callout (Page 3) | Entry barrier for electric two-wheelers (Ola S1 X Gen 3 2 kWh). |
| **Market Price Ceiling** | `[Maximum Product Price]` | `FactProductMetrics[price]` | Verified | **Available (₹169,999)** | Card / Range Callout (Page 3) | Top-tier flagship commuter pricing (Ola S1 Pro Plus 5.3 kWh). |
| **Average Range** | `[Average Certified Range]` | `FactProductMetrics[certified_range_km]` | Verified | **Available (156.5 km)** | Single Value Card (Page 1) | IDC/ARAI certified range expectation for consumer commuting. |
| **Average Battery** | `[Average Battery Capacity]` | `FactProductMetrics[battery_kwh]` | Verified | **Available (3.54 kWh)** | Single Value Card (Page 1) | Average physical energy storage per vehicle. |
| **Average Top Speed** | `[Average Top Speed]` | `FactProductMetrics[top_speed_kmph]` | Verified | **Available (87.8 km/h)** | Card / Gauge (Pages 1, 4) | Performance benchmark indicating dominance of high-speed scooters. |
| **Average Motor Power** | `[Average Motor Power]` | `FactProductMetrics[motor_power_kw]` | Verified | **Available (7.29 kW)** | Clustered Column (Page 2) | Powertrain capacity across competitive offerings. |
| **Range Cost Efficiency** | `[Average Price per KM]` | `FactProductMetrics[price_per_km]` | Verified | **Available (₹839.95/km)** | Scatter / Table (Page 3) | Core consumer value metric: capital cost per certified range km. |
| **Battery Cost Efficiency** | `[Average Price per KWh]` | `FactProductMetrics[price_per_kwh]` | Verified | **Available (₹35,871/kWh)** | Scatter / Bar Chart (Page 3) | OEM engineering cost efficiency: ex-showroom price per unit battery. |
| **Portfolio Concentration HHI** | `[Product Portfolio HHI]` | `FactProductMetrics[product]` | Verified | **Available (2,333.3)** | Card / Gauge (Page 2) | Offering concentration across OEMs (2,333 indicates moderately concentrated). |
| **Budget Product Count** | `[Budget Product Count]` | `ProductPositioning[price_bucket]` | Verified | **Available (3)** | Donut Chart (Page 4) | Vehicles under ₹100,000 (Bajaj Chetak C2501, TVS iQube 2.3, Ola S1 X 2kWh). |
| **Mid-Market Product Count** | `[Mid-Market Product Count]` | `ProductPositioning[price_bucket]` | Verified | **Available (19)** | Donut Chart (Page 4) | Dominant mainstream adoption tier (₹100,000 to ₹180,000). |
| **Long-Range Model Count** | `[Long-Range Product Count]` | `ProductPositioning[range_bucket]` | Verified | **Available (4)** | Donut / Bar Chart (Page 4) | Vehicles with certified range > 180 km (Ola S1 X Plus, TVS iQube ST). |
| **High-Performance Count** | `[High-Performance Product Count]` | `ProductPositioning[performance_bucket]` | Verified | **Available (7)** | Stacked Bar (Page 4) | Vehicles capable of speeds > 90 km/h. |

---

## 3. Pending Market & Strategic KPIs (Fail-Closed Templates)

In strict accordance with the project's **provenance safeguard policy**, market-registration metrics are marked as pending. The dashboard surfaces their status explicitly to maintain data integrity.

| KPI Name | DAX Measure | Target Source Table | Verification Status | Current Availability | Intended Dashboard Visual | Planned Business Interpretation |
| :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| **Total EV Registrations** | `[Total EV Registrations (Pending)]` | `PendingMarketRegistrations[Registrations]` | Pending Vahan Export | **PENDING** | KPI Card (Disabled / "Pending") | Total annualized e2W volume registered across India. |
| **YoY Market Growth %** | `[YoY Market Growth Pct (Pending)]` | `PendingMarketRegistrations` | Pending Vahan Export | **PENDING** | KPI Card (Disabled / "Pending") | Annualized rate of market volume expansion. |
| **Market CAGR %** | `[Market CAGR Pct (Pending)]` | `PendingMarketRegistrations` | Pending Vahan Export | **PENDING** | Callout Banner (Page 5) | Multi-year structural growth velocity. |
| **EV Penetration %** | `[EV Penetration Pct (Pending)]` | `PendingMarketRegistrations` | Pending Vahan Export | **PENDING** | Gauge (Page 5) | e2W share of total two-wheeler registrations. |
| **OEM Market Share %** | `[OEM Registration Market Share Pct (Pending)]` | `PendingMarketRegistrations` | Pending Vahan Export | **PENDING** | 100% Stacked Bar (Page 5) | Volume commercial market share per competitor. |
| **Market Volume HHI** | `[Market Volume HHI (Pending)]` | `PendingMarketRegistrations` | Pending Vahan Export | **PENDING** | Gauge (Page 5) | Industry concentration based on actual registration volume. |
| **State Attractiveness Rank** | `[State Registration Rank (Pending)]` | `PendingMarketRegistrations` | Pending Vahan Export | **PENDING** | Ranked Table (Page 5) | Econometric state prioritization for regional rollout. |
