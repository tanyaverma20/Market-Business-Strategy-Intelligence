# Power BI 5-Page Dashboard Specification: Indian Electric 2W Market

## 1. Executive Summary & Design System

This document specifies the exact visual composition, layout, field assignments, interactivity rules, and styling standards for the **5-page Power BI Executive Dashboard Suite**.

### Consulting-Grade Design System
- **Layout Grid**: 16:9 widescreen canvas (`1920 x 1080 px` or `1280 x 720 px`).
- **Color Palette**:
  - Primary Slate / Charcoal: `#1E293B` (Cards, Headers, KPI Values)
  - Accent Teal / Electric Blue: `#0EA5E9` (Primary Series, Bars, Focus Points)
  - Secondary Emerald Green: `#10B981` (High Efficiency, Budget / Value Tier)
  - Warning Amber: `#F59E0B` (Mid-Market / Moderate Flags)
  - Inactive / Pending Gray: `#94A3B8` (Disabled / Pending Data Elements)
  - Clean Background: `#F8FAFC` (Canvas Background)
  - Container Background: `#FFFFFF` with subtle 1px border (`#E2E8F0`) and 4px rounded corners.
- **Typography**: Segoe UI / Segoe UI Semibold (Standard Power BI executive font family).
- **Navigation**: Left-side vertical navigation rail or top persistent tab bar.

---

## 2. Page 1 — Executive Market & Business Overview

### 2.1 Purpose & Strategic Intent
Delivers an immediate, C-suite synthesis of the verified Indian Electric 2-Wheeler product landscape while transparently reporting that official Vahan registration market data remains pending.

### 2.2 Header & Context Banner
- **Title**: `Indian Electric 2-Wheeler Market Intelligence — Executive Overview`
- **Subtitle**: `Verified Product Catalog & Competitive Portfolio Benchmark (2025–2026 Models)`
- **Data Status Banner**: Top-right badge displaying:
  - `Product Data: VERIFIED (30 Models / 5 OEMs)` (Green)
  - `Market Registrations: PENDING VERIFIED VAHAN DATA` (Amber)

### 2.3 Visual Layout & Specifications

#### 1. Top KPI Card Strip (5 Cards)
- **Visual 1.1: Active Manufacturers**
  - Type: Single Value KPI Card
  - Measure: `[Total Manufacturers]`
  - Format: `5 OEMs`
  - Subtitle: `Ather, Bajaj, Ola, TVS, Ampere`
- **Visual 1.2: Verified Products**
  - Type: Single Value KPI Card
  - Measure: `[Total Products]`
  - Format: `30 Models`
  - Subtitle: `22 Priced / 8 Variant Specs`
- **Visual 1.3: Benchmark Market Price**
  - Type: Single Value KPI Card
  - Measure: `[Average Product Price]`
  - Format: `₹1,24,466`
  - Subtitle: `Median: ₹1,26,078`
- **Visual 1.4: Benchmark Certified Range**
  - Type: Single Value KPI Card
  - Measure: `[Average Certified Range]`
  - Format: `156.5 km`
  - Subtitle: `IDC / ARAI Certified`
- **Visual 1.5: Benchmark Battery Pack**
  - Type: Single Value KPI Card
  - Measure: `[Average Battery Capacity]`
  - Format: `3.54 kWh`
  - Subtitle: `Energy: 22.6 Wh/km`

#### 2. Visual 1.6: OEM Portfolio Breadth & Catalog Share
- **Visual Type**: Clustered Horizontal Bar Chart
- **Title**: `Verified Product Portfolio Size by Manufacturer`
- **Y-Axis**: `DimManufacturer[manufacturer]` (Sorted descending by count)
- **X-Axis**: `[Total Products]`
- **Tooltip**: `[Average Product Price]`, `[Average Certified Range]`, `DimManufacturer[mfg_portfolio_share_pct]`
- **Key Insight**: Ola Electric leads with 9 models (30.0%), followed by Ather (8 models, 26.7%), TVS (6 models, 20.0%), Bajaj (5 models, 16.7%), and Ampere (2 models, 6.7%).

#### 3. Visual 1.7: OEM Average Pricing vs. Market Benchmark
- **Visual Type**: Clustered Column Chart with Benchmark Line
- **Title**: `Average Ex-Showroom Price by Manufacturer vs. Market Average`
- **X-Axis**: `DimManufacturer[manufacturer]`
- **Y-Axis**: `[Average Product Price]`
- **Constant Line / Measure**: `[Market Benchmark Average Price]` (₹124,466, dashed line)
- **Key Insight**: Ather (₹131,127) and Ola (₹130,142) operate above market average, while TVS (₹116,876) and Bajaj (₹116,168) maintain disciplined mass-market pricing below the benchmark.

#### 4. Visual 1.8: Verified Strategic Insights Callout Box
- **Visual Type**: Rich Text / Multi-Row Card Callout
- **Title**: `Verified Executive Takeaways`
- **Content**:
  - `1. Portfolio Concentration`: Moderately concentrated catalog (HHI: 2,333.3) dominated by top 3 players holding 76.7% of models.
  - `2. Price Band`: ₹85k spread from ₹84,999 (Ola S1 X 2kWh) to ₹169,999 (Ola S1 Pro Plus 5.3kWh).
  - `3. Mass Adoption Sweet Spot`: 86% of priced models occupy the ₹100k–₹150k band.

---

## 3. Page 2 — Product & Competitive Intelligence

### 3.1 Business Question Answered
*"How does the verified product landscape compare across manufacturers in specifications, pricing tiers, and powertrain capacity?"*

### 3.2 Visual Layout & Specifications

#### 1. Visual 2.1: Multi-Metric OEM Specification Comparison
- **Visual Type**: Matrix / Heatmap Table
- **Title**: `Competitive Specification Matrix by Manufacturer`
- **Rows**: `DimManufacturer[manufacturer]`
- **Values**:
  - `[Total Products]`
  - `[Priced Products Count]`
  - `[Average Product Price]` (Formatted `₹#,##0`)
  - `[Average Certified Range]` (Formatted `0.0 km`)
  - `[Average Battery Capacity]` (Formatted `0.00 kWh`)
  - `[Average Top Speed]` (Formatted `0.0 km/h`)
  - `[Average Motor Power]` (Formatted `0.0 kW`)
  - `[Average Price per KM]` (Formatted `₹#,##0.00 / km`)

#### 2. Visual 2.2: OEM Price Band Distribution (Min, Median, Max)
- **Visual Type**: Clustered Range Column / Box-and-Whisker Style Chart
- **Title**: `Price Band Span by OEM (Min, Median, Max)`
- **X-Axis**: `DimManufacturer[manufacturer]`
- **Values**: `[Minimum Product Price]`, `[Median Product Price]`, `[Maximum Product Price]`
- **Interpretation**: Illustrates portfolio pricing strategy: Ola spans the entire market (₹85k–₹170k), Ather targets mid-to-premium (₹108k–₹150k), TVS clusters between ₹95k and ₹147k across 6 battery steps.

#### 3. Visual 2.3: Competitive Ranking & Product Drill-Down Matrix
- **Visual Type**: Interactive Grid Table with Slicers
- **Title**: `Granular Product Rankings & Specifications`
- **Columns**:
  - `FactProductMetrics[product]`
  - `DimProduct[manufacturer]`
  - `CompetitiveAnalysis[manufacturer_rank]`
  - `CompetitiveAnalysis[product_rank]`
  - `FactProductMetrics[price]`
  - `FactProductMetrics[certified_range_km]`
  - `FactProductMetrics[battery_kwh]`
  - `FactProductMetrics[top_speed_kmph]`
  - `CompetitiveAnalysis[price_efficiency_rank]`

---

## 4. Page 3 — Pricing & Value Analysis

### 4.1 Business Question Answered
*"Which verified products provide superior measurable consumer value for their price?"*

### 4.2 Visual Layout & Specifications

#### 1. Visual 3.1: Range Cost Efficiency vs. Battery Cost Efficiency
- **Visual Type**: Scatter Plot (Bubble Chart)
- **Title**: `Range Cost Efficiency (₹/km) vs. Battery Cost Efficiency (₹/kWh)`
- **X-Axis**: `FactProductMetrics[price_per_km]` (Lower is better)
- **Y-Axis**: `FactProductMetrics[price_per_kwh]` (Lower is better)
- **Size / Bubble Size**: `FactProductMetrics[battery_kwh]`
- **Legend / Color**: `DimProduct[manufacturer]`
- **Tooltips**: `FactProductMetrics[product]`, `FactProductMetrics[price]`, `FactProductMetrics[certified_range_km]`
- **Quadrant Interpretation**:
  - **Bottom-Left (Superior Value Sweet Spot)**: Ola S1 X Plus Gen 3 5.2 kWh (₹406/km, ₹25,000/kWh), TVS iQube ST 5.3 kWh (₹693/km, ₹27,713/kWh).
  - **Top-Right (Premium / Lower Spec Efficiency)**: Ampere Nexus ST (₹1,315/km, ₹43,833/kWh), Ather Rizta Z 2.9 kWh (₹1,054/km, ₹44,709/kWh).

#### 2. Visual 3.2: Price Quartile & Relative Positioning Breakdown
- **Visual Type**: 100% Stacked Bar Chart
- **Title**: `Price Positioning Distribution by Manufacturer`
- **Y-Axis**: `DimManufacturer[manufacturer]`
- **X-Axis**: `[Total Products]` (Normalized to 100%)
- **Legend**: `PricingAnalysis[relative_price_position]`
  - Green: `below market average`
  - Amber: `above market average`
  - Gray: `unpriced / pending`

#### 3. Visual 3.3: Top 10 Price-Efficiency Leaderboard
- **Visual Type**: Ranked Bar Chart
- **Title**: `Top 10 Most Range-Cost-Efficient Models (Lowest ₹ per km)`
- **Y-Axis**: `FactProductMetrics[product]` (Sorted ascending by ₹/km)
- **X-Axis**: `FactProductMetrics[price_per_km]`
- **Data Labels**: Enabled (`₹406`, `₹500`, `₹693`, `₹745`, `₹760`)

---

## 5. Page 4 — Product Positioning & Whitespace Analysis

### 5.1 Business Question Answered
*"Where are products positioned across price, range, and battery brackets, and where does unserved whitespace exist?"*

### 5.2 Visual Layout & Specifications

#### 1. Visual 4.1: Product Positioning Scatter Grid (Price vs. Certified Range)
- **Visual Type**: 4-Quadrant Scatter Plot
- **Title**: `Price vs. Certified Range: Competitive Clustering & Whitespace`
- **X-Axis**: `FactProductMetrics[certified_range_km]` (50 km to 350 km)
- **Y-Axis**: `FactProductMetrics[price]` (₹80,000 to ₹180,000)
- **Legend**: `ProductPositioning[price_bucket]`
- **Reference Lines**:
  - Median Range: 153 km (Vertical line)
  - Median Price: ₹126,078 (Horizontal line)

#### 2. Visual 4.2: Whitespace Analysis Callout
- **Visual Type**: Highlight Card / Callout Box
- **Title**: `Identified Commercial Whitespace`
- **Key Findings**:
  - `Whitespace 1: Budget Standard-Range (< ₹100k, 120–180 km)`: **Completely unoccupied.** All models under ₹100k offer < 120 km range. An offering at ₹95k with 130 km range captures unmet commuter demand.
  - `Whitespace 2: Premium Inter-City (> 200 km, ₹160k+)`: Currently occupied solely by Ola S1 X Plus 5.2kWh and TVS iQube ST. Legacy OEMs have no multi-variant presence in ultra-long-range commuting.

#### 3. Visual 4.3: Catalog Segmentation Breakdown
- **Visual Type**: Donut Chart / Decomposition Tree
- **Title**: `Catalog Share by Price Tier & Range Tier`
- **Levels**: `ProductPositioning[price_bucket]` -> `ProductPositioning[range_bucket]`
- **Values**: `[Total Products]`
- **Breakdown**: Budget (3 models, 10%), Mid-Market (19 models, 63%), Unpriced (8 models, 27%).

---

## 6. Page 5 — Strategy & Opportunity Framework

### 6.1 Purpose & Safeguard Notice
Synthesizes the strategic entry evaluation while explicitly alerting executives that macroeconomic state registration and localized subsidy datasets remain fail-closed pending official Vahan exports.

### 6.2 Header Callout
> **DATA PROVENANCE SAFEGUARD**: State-level registrations and dealer-level cost data remain **PENDING VERIFIED VAHAN DATA**. The frameworks below present the verified product-side intelligence combined with the formal evaluation architecture ready to ingest official market series.

### 6.3 Visual Layout & Specifications

#### 1. Visual 5.1: Strategic Entry Sweet Spot Matrix
- **Visual Type**: Matrix Table
- **Title**: `Alpha Motors Recommended Product Entry Configuration`
- **Dimensions**:
  - Target Price Band: `₹1,15,000 – ₹1,25,000` (Mid-market value tier)
  - Target Battery Capacity: `3.5 – 4.0 kWh`
  - Target Certified Range: `140 – 160 km` (IDC)
  - Target Top Speed: `80 – 85 km/h`
  - Target Price per KM: `₹750 – ₹820 / km`
  - Strategic Benchmark: Positioned directly against TVS iQube 3.5 kWh and Ather Rizta S.

#### 2. Visual 5.2: Geographic Attractiveness Index (GAI) Framework Architecture
- **Visual Type**: Process Card / Model Flow
- **Title**: `Geographic Opportunity Prioritization Model (Ready for Vahan Ingestion)`
- **Framework Weights**:
  - e2W Registration Volume & Growth: `30%` (Pending Vahan)
  - Per Capita State Income: `25%` (Verified RBI/NITI Aayog)
  - Two-Wheeler Density: `20%` (Verified MoRTH)
  - State EV Policy & PM E-DRIVE Alignment: `15%` (Verified Policy Timeline)
  - Urban Agglomeration Density: `10%` (Census)

#### 3. Visual 5.3: Unit Economics & Contribution Margin Sensitivity
- **Visual Type**: Waterfall / Scenario Bar Chart
- **Title**: `Unit Economics Sensitivity Framework (Base / Conservative / Optimistic)`
- **Scenarios**:
  - Target Ex-Showroom ASP: `₹1,20,000`
  - Target Battery Cost (@ $115/kWh): `~₹38,000 – ₹42,000`
  - Target Contribution Margin: `18% – 22%` post-PM E-DRIVE rationalization.

---

## 7. Interactive Filtering & Slicer System

A synchronized slicer bar is anchored at the top of Pages 1–4:

| Slicer Name | Source Column | Selection Mode | Visual Type | Default State |
| :--- | :--- | :---: | :---: | :---: |
| **Manufacturer** | `DimManufacturer[manufacturer]` | Multi-Select | Dropdown / Tile | `All` |
| **Price Tier** | `ProductPositioning[price_bucket]` | Multi-Select | Horizontal Buttons | `All` |
| **Range Bracket** | `ProductPositioning[range_bucket]` | Multi-Select | Horizontal Buttons | `All` |
| **Top Speed Class** | `ProductPositioning[performance_bucket]` | Multi-Select | Dropdown | `All` |

### Cross-Filtering & Drill-Through Behavior
1. **Cross-Filtering**: Clicking any OEM bar on Page 1 or 2 cross-filters the entire canvas to show that OEM's specific models, price distributions, and quadrant positioning.
2. **Drill-Through**: Right-clicking any model in the Visual 2.3 or 3.1 scatter plot enables drill-through to a detailed **Product Specification Card** detailing provenance URL, access date, and certified test standard.

---

## 8. Complete Power BI Desktop Assembly Manual

To build this report manually in Power BI Desktop:
1. **Launch Power BI Desktop** (Empty project).
2. **Open Power Query**: Home > Transform Data > Advanced Editor.
3. **Execute M Scripts**: Follow [`docs/POWER_BI_POWER_QUERY.md`](file:///c:/Users/Tanya%20Verma/OneDrive/Desktop/Market-Business-Strategy-Intelligence/docs/POWER_BI_POWER_QUERY.md) and load all 7 verified tables.
4. **Create Model Relationships**: Go to Model View and verify the 1:* and 1:1 single-direction relationships defined in [`docs/POWER_BI_MODEL.md`](file:///c:/Users/Tanya%20Verma/OneDrive/Desktop/Market-Business-Strategy-Intelligence/docs/POWER_BI_MODEL.md).
5. **Create DAX Measures**: Go to Report View > Modeling > New Measure, copy-pasting the 24 verified measures from [`powerbi/dax_measures.dax`](file:///c:/Users/Tanya%20Verma/OneDrive/Desktop/Market-Business-Strategy-Intelligence/powerbi/dax_measures.dax).
6. **Create the 5 Pages**: Add 5 tabs with the exact names and visual compositions detailed in Sections 2 through 6 above.
7. **Save Project**: Save as `Market-Business-Strategy-Intelligence.pbix`.
