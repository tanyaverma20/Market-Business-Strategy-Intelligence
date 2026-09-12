# Power BI Data Model Specification: Indian Electric 2-Wheeler Market

## 1. Executive Summary & Architecture

The Power BI data model follows a **Star Schema** architecture tailored for analytical clarity, high query performance, and strict compliance with the project's **provenance safeguard policy**. 

The model segregates dimensional attributes from core numerical performance facts and extends them via 1:1 analytical mart tables. Disconnected benchmark tables house KPI audit trails, while pending market registration schemas remain completely isolated and fail-closed with 0 records.

```
                    ┌─────────────────────────┐
                    │     DimManufacturer     │
                    │   (OEM Hierarchy & PK)  │
                    └────────────┬────────────┘
                                 │ 1
                                 │
                                 │ * (Single Direction)
                                 ▼
┌──────────────────────┐    ┌─────────────────────────┐    ┌──────────────────────┐
│      DimProduct      │ 1  │   FactProductMetrics    │  1 │ CompetitiveAnalysis  │
│  (Catalog Dimension) ├────┤  (Core Metrics & Ratios)├───►│ (Rankings & Windows) │
└──────────────────────┘ *  └────────────┬────────────┘ 1  └──────────────────────┘
                                         │ 1
                                         ├─────────────────────────┐
                                         │ 1                       │ 1
                                         ▼                         ▼
                            ┌─────────────────────────┐    ┌──────────────────────┐
                            │     PricingAnalysis     │    │  ProductPositioning  │
                            │ (Percentiles & Quarts)  │    │  (Buckets & Segments)│
                            └─────────────────────────┘    └──────────────────────┘

            ┌─────────────────────────┐    ┌──────────────────────────────────┐
            │        KPIStatus        │    │    PendingMarketRegistrations    │
            │  (Benchmark KPI Audit)  │    │   (0 Rows — Fail-Closed Schema)  │
            └─────────────────────────┘    └──────────────────────────────────┘
```

---

## 2. Table Specifications

### 2.1 Dimension Tables

#### `DimManufacturer`
- **Purpose**: Conformed dimension providing OEM-level hierarchy, verification status, and portfolio totals.
- **Source**: `data/processed/sql/sql_competitive_analysis.csv` (grouped by OEM).
- **Primary Key**: `manufacturer` (Text)
- **Columns**:
  - `manufacturer` (PK, Text): Standardized OEM name (e.g., Ather Energy, Bajaj Auto, Ola Electric, TVS Motor Company, Ampere).
  - `mfg_product_count` (Integer): Total distinct verified products offered.
  - `mfg_portfolio_share_pct` (Decimal): Percentage of total verified catalog models (e.g., 30.0% for Ola, 26.7% for Ather).
  - `verification_status` (Text): Data audit status (`verified`).
  - `Data_Ingestion_Date` (Date): Audit date of data load.

#### `DimProduct`
- **Purpose**: Product master dimension detailing commercial model names, categories, and audit flags.
- **Source**: `data/processed/sql/sql_competitive_analysis.csv` (unique products).
- **Primary Key**: `product` (Text)
- **Foreign Key**: `manufacturer` -> `DimManufacturer[manufacturer]`
- **Columns**:
  - `product` (PK, Text): Unique commercial model name (e.g., `S1 X Plus Gen 3 5.2 kWh`, `iQube ST 5.3 kWh`).
  - `manufacturer` (FK, Text): Associated OEM.
  - `category` (Text): Vehicle classification (`electric scooter`).
  - `verification_status` (Text): Provenance tag (`verified`).
  - `Is_Verified_Catalog` (Boolean): Boolean flag enforcing verified status (`TRUE`).

---

### 2.2 Fact Table

#### `FactProductMetrics`
- **Purpose**: Central analytical fact table containing technical specifications, pricing, and derived performance ratios.
- **Source**: `data/processed/sql/sql_competitive_analysis.csv`
- **Primary Key**: `product` (Text)
- **Foreign Keys**:
  - `product` -> `DimProduct[product]`
  - `manufacturer` -> `DimManufacturer[manufacturer]`
- **Columns**:
  - `product` (PK, FK, Text)
  - `manufacturer` (FK, Text)
  - `price` (Currency / Decimal): Ex-showroom price in INR. Nullable for unpriced catalog models.
  - `battery_kwh` (Decimal): Usable/nominal battery pack capacity in kWh.
  - `certified_range_km` (Decimal): ARAI/IDC certified range in kilometers.
  - `top_speed_kmph` (Decimal): Certified top speed in km/h.
  - `motor_power_kw` (Decimal): Peak motor power output in kW.
  - `price_per_km` (Currency / Decimal): Pre-calculated ex-showroom price per certified kilometer.
  - `price_per_kwh` (Currency / Decimal): Pre-calculated ex-showroom price per kWh battery capacity.
  - `energy_efficiency_wh_per_km` (Decimal): Energy consumption ratio: `(battery_kwh * 1000) / certified_range_km`.
  - `verification_status` (Text): Provenance tag (`verified`).

---

### 2.3 Analytical Extension Tables (1:1 Relationships)

#### `CompetitiveAnalysis`
- **Purpose**: Multi-dimensional ranking extensions answering competitive positioning questions.
- **Source**: `data/processed/sql/sql_competitive_analysis.csv`
- **Primary Key**: `product` (Text)
- **Columns**:
  - `product` (PK, FK, Text)
  - `manufacturer` (Text)
  - `manufacturer_rank` (Integer): Price rank of model within its manufacturer (1 = lowest entry price).
  - `product_rank` (Integer): Overall market-wide price hierarchy.
  - `price_efficiency_rank` (Integer): Rank based on lowest ₹/km (1 = most range efficient).
  - `range_rank` (Integer): Rank based on certified IDC range (1 = highest range).
  - `speed_rank` (Integer): Rank based on maximum speed.
  - `mfg_portfolio_share_pct` (Decimal): OEM percentage share of verified offerings.

#### `PricingAnalysis`
- **Purpose**: Price distribution metrics, quartiles, percentiles, and market premium flags.
- **Source**: `data/processed/sql/sql_pricing_analysis.csv`
- **Primary Key**: `product` (Text)
- **Columns**:
  - `product` (PK, FK, Text)
  - `manufacturer` (Text)
  - `price` (Currency / Decimal)
  - `price_percentile` (Decimal): 0.0 to 1.0 distribution percentile.
  - `price_quartile` (Integer): 1 to 4 quartile indicator.
  - `product_price_rank` (Integer): Price rank descending.
  - `avg_market_price` (Currency / Decimal): Overall market benchmark average (₹124,466.14).
  - `mfg_avg_price` (Currency / Decimal): OEM average price benchmark.
  - `relative_price_position` (Text): Classification (`below market average`, `above market average`, `unpriced / pending`).
  - `price_premium_vs_market_pct` (Decimal): Percentage variance from catalog benchmark average.

#### `ProductPositioning`
- **Purpose**: Multi-axial segmentation across price tiers, range brackets, and performance bands.
- **Source**: `data/processed/sql/sql_product_positioning.csv`
- **Primary Key**: `product` (Text)
- **Columns**:
  - `product` (PK, FK, Text)
  - `manufacturer` (Text)
  - `price_bucket` (Text): `budget` (< ₹100k), `mid-market` (₹100k–₹180k), `premium` (> ₹180k), `unpriced`.
  - `range_bucket` (Text): `short-range` (< 120km), `standard-range` (120–180km), `long-range` (> 180km).
  - `battery_bucket` (Text): `compact-battery` (< 3.0kWh), `standard-battery` (3.0–4.5kWh), `high-battery` (> 4.5kWh).
  - `performance_bucket` (Text): `entry` (< 70km/h), `balanced` (70–90km/h), `high-performance` (> 90km/h).
  - `positioning_summary` (Text): Combined descriptor (e.g., `mid-market / long-range`).
  - `manufacturer_product_rank` (Integer)
  - `manufacturer_budget_count` (Integer)
  - `manufacturer_midmarket_count` (Integer)
  - `manufacturer_premium_count` (Integer)

---

### 2.4 Disconnected Tables

#### `KPIStatus`
- **Purpose**: Centralized verified KPI register for executive scorecards and methodology audit.
- **Source**: `data/processed/sql/sql_kpi_results.csv`
- **Primary Key**: `kpi_name` (Text)
- **Columns**: `kpi_name`, `value`, `unit`, `source`, `verification_status`, `calculation_date`, `methodology`.

#### `PendingMarketRegistrations`
- **Purpose**: Fail-closed schema table for future Vahan registration data.
- **Source**: Empty M table schema.
- **Row Count**: **0 (strictly empty)**.
- **Columns**: `Date`, `Month`, `Year`, `State`, `VehicleCategory`, `FuelType`, `Manufacturer`, `Registrations`, `Source`, `VerificationStatus`.

---

## 3. Relationships & Cardinality

| From Table | From Column | To Table | To Column | Cardinality | Filter Direction | Active | Rationale |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| `DimManufacturer` | `manufacturer` | `FactProductMetrics` | `manufacturer` | 1 : * | Single (Dim -> Fact) | Yes | Standard star-schema filtering from OEM dimension down to facts. |
| `DimProduct` | `product` | `FactProductMetrics` | `product` | 1 : * | Single (Dim -> Fact) | Yes | Product dimension filtering facts. |
| `FactProductMetrics` | `product` | `CompetitiveAnalysis` | `product` | 1 : 1 | Single (Fact -> Dim) | Yes | 1:1 extension table containing window rankings. |
| `FactProductMetrics` | `product` | `PricingAnalysis` | `product` | 1 : 1 | Single (Fact -> Dim) | Yes | 1:1 extension table containing pricing quartiles and percentiles. |
| `FactProductMetrics` | `product` | `ProductPositioning` | `product` | 1 : 1 | Single (Fact -> Dim) | Yes | 1:1 extension table containing segmentation buckets. |

### Rationale for Single-Direction Filtering
Bidirectional cross-filtering is **strictly prohibited** in this model. Bidirectional relationships introduce filter context ambiguity, can cause unintentional circular dependency paths, degrade in-memory DAX performance, and create unpredictable results when combined with complex window or ranking calculations (`RANKX`, `ALL`, `ALLEXCEPT`).

---

## 4. Modeling Strategy: Calculated Columns vs Measures

1. **Calculated Columns** (Used sparingly):
   - Only used for categorical slicing attributes that must appear in visual axis, legends, or slicers:
     - `energy_efficiency_wh_per_km` (physical ratio)
     - `Is_Verified_Catalog` (audit flag)
2. **DAX Measures** (Preferred for all analytics):
   - All aggregations, price spreads, percentiles, portfolio shares, and benchmarks are implemented as dynamic DAX measures.
   - Ensures responsive calculation under any interactive filter context (OEM, Category, Segment, Price Quartile).
