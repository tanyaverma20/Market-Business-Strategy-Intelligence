# Power BI DAX Analytics Measure Library: Indian Electric 2W Market

## 1. Overview & DAX Design Philosophy

The DAX measure library provides the analytical engine for the 5-page Power BI executive dashboard. All measures adhere to the following principles:

1. **Strict Data Verification**: Measures are computed **only** against verified primary data. No proxy or fabricated numbers are generated.
2. **Dynamic Context-Awareness**: Measures utilize proper filter context transitions (`CALCULATE`, `ALL`, `ALLEXCEPT`, `FILTER`) to ensure accurate calculation when sliced by OEM, price bucket, range band, or performance tier.
3. **Defensive Numerics**: Divisions use `DIVIDE(..., BLANK())` or explicit 0 fallbacks to prevent division-by-zero errors.
4. **Explicit Fail-Closed Market Isolation**: Future registration and market growth measures return `BLANK()` with documented comments rather than returning unverified proxy numbers.

---

## 2. Core Portfolio & Volume Measures (Verified)

### 2.1 `[Total Products]`
- **DAX Formula**:
  ```dax
  Total Products = 
  DISTINCTCOUNT(FactProductMetrics[product])
  ```
- **Return Type**: Whole Number (Formatted as `#,##0`)
- **Business Purpose**: Counts verified EV two-wheeler commercial models available in the market (30 total).

### 2.2 `[Total Manufacturers]`
- **DAX Formula**:
  ```dax
  Total Manufacturers = 
  DISTINCTCOUNT(DimManufacturer[manufacturer])
  ```
- **Return Type**: Whole Number
- **Business Purpose**: Tracks active competing OEMs verified in the catalog (5 OEMs: Ola, Ather, TVS, Bajaj, Ampere).

### 2.3 `[Priced Products Count]`
- **DAX Formula**:
  ```dax
  Priced Products Count = 
  CALCULATE(
      COUNTROWS(FactProductMetrics),
      NOT(ISBLANK(FactProductMetrics[price]))
  )
  ```
- **Return Type**: Whole Number
- **Business Purpose**: Counts models where official ex-showroom pricing is captured (22 models).

### 2.4 `[Average Manufacturer Portfolio Size]`
- **DAX Formula**:
  ```dax
  Average Manufacturer Portfolio Size = 
  DIVIDE([Total Products], [Total Manufacturers], 0)
  ```
- **Return Type**: Decimal (`0.0`)
- **Business Purpose**: Measures portfolio breadth per competitor (averages 6.0 models per OEM).

---

## 3. Pricing & Value Analysis Measures (Verified)

### 3.1 `[Average Product Price]`
- **DAX Formula**:
  ```dax
  Average Product Price = 
  AVERAGE(FactProductMetrics[price])
  ```
- **Return Type**: Currency (Formatted as `₹#,##0`)
- **Business Purpose**: Benchmark ex-showroom price across priced models (Catalog average: ₹124,466).

### 3.2 `[Median Product Price]`
- **DAX Formula**:
  ```dax
  Median Product Price = 
  MEDIAN(FactProductMetrics[price])
  ```
- **Return Type**: Currency (Formatted as `₹#,##0`)
- **Business Purpose**: 50th percentile price point resilient against premium skew (Catalog median: ₹126,078).

### 3.3 `[Minimum Product Price]`
- **DAX Formula**:
  ```dax
  Minimum Product Price = 
  MIN(FactProductMetrics[price])
  ```
- **Return Type**: Currency (Formatted as `₹#,##0`)
- **Business Purpose**: Market floor price (₹84,999 — Ola S1 X Gen 3 2 kWh).

### 3.4 `[Maximum Product Price]`
- **DAX Formula**:
  ```dax
  Maximum Product Price = 
  MAX(FactProductMetrics[price])
  ```
- **Return Type**: Currency (Formatted as `₹#,##0`)
- **Business Purpose**: Market ceiling price (₹169,999 — Ola S1 Pro Plus Gen 3 5.3 kWh).

### 3.5 `[Price Spread INR]`
- **DAX Formula**:
  ```dax
  Price Spread INR = 
  [Maximum Product Price] - [Minimum Product Price]
  ```
- **Return Type**: Currency (Formatted as `₹#,##0`)
- **Business Purpose**: Absolute market price band (₹85,000 spread).

### 3.6 `[Market Benchmark Average Price]`
- **DAX Formula**:
  ```dax
  Market Benchmark Average Price = 
  CALCULATE(
      [Average Product Price],
      ALL(FactProductMetrics)
  )
  ```
- **Return Type**: Currency (Formatted as `₹#,##0`)
- **Business Purpose**: Unfiltered catalog benchmark for relative premium calculations.

### 3.7 `[Price Premium vs Market Pct]`
- **DAX Formula**:
  ```dax
  Price Premium vs Market Pct = 
  VAR MarketAvg = [Market Benchmark Average Price]
  RETURN
  DIVIDE(
      [Average Product Price] - MarketAvg,
      MarketAvg,
      BLANK()
  )
  ```
- **Return Type**: Percentage (Formatted as `+0.0%;-0.0%;0.0%`)
- **Business Purpose**: Evaluates whether an OEM or product segment commands a premium or discount relative to the market average.

---

## 4. Technical Performance & Efficiency Measures (Verified)

### 4.1 `[Average Battery Capacity]`
- **DAX Formula**:
  ```dax
  Average Battery Capacity = 
  AVERAGE(FactProductMetrics[battery_kwh])
  ```
- **Return Type**: Decimal (`0.00` kWh)
- **Business Purpose**: Mean battery capacity (Catalog average: 3.54 kWh).

### 4.2 `[Average Certified Range]`
- **DAX Formula**:
  ```dax
  Average Certified Range = 
  AVERAGE(FactProductMetrics[certified_range_km])
  ```
- **Return Type**: Decimal (`0.0` km)
- **Business Purpose**: Mean IDC/ARAI certified range (Catalog average: 156.5 km).

### 4.3 `[Average Top Speed]`
- **DAX Formula**:
  ```dax
  Average Top Speed = 
  AVERAGE(FactProductMetrics[top_speed_kmph])
  ```
- **Return Type**: Decimal (`0.0` km/h)
- **Business Purpose**: Mean maximum vehicle velocity (Catalog average: 87.8 km/h).

### 4.4 `[Average Motor Power]`
- **DAX Formula**:
  ```dax
  Average Motor Power = 
  AVERAGE(FactProductMetrics[motor_power_kw])
  ```
- **Return Type**: Decimal (`0.0` kW)
- **Business Purpose**: Mean peak motor output (Catalog average: 7.29 kW).

### 4.5 `[Average Price per KM]`
- **DAX Formula**:
  ```dax
  Average Price per KM = 
  AVERAGE(FactProductMetrics[price_per_km])
  ```
- **Return Type**: Currency (Formatted as `₹#,##0.00 / km`)
- **Business Purpose**: Range cost efficiency benchmark (Catalog average: ₹839.95 / km).

### 4.6 `[Average Price per KWh]`
- **DAX Formula**:
  ```dax
  Average Price per KWh = 
  AVERAGE(FactProductMetrics[price_per_kwh])
  ```
- **Return Type**: Currency (Formatted as `₹#,##0 / kWh`)
- **Business Purpose**: Battery capital cost efficiency benchmark (Catalog average: ₹35,871 / kWh).

### 4.7 `[Weighted Fleet Energy Efficiency]`
- **DAX Formula**:
  ```dax
  Weighted Fleet Energy Efficiency = 
  DIVIDE(
      SUM(FactProductMetrics[battery_kwh]) * 1000.0,
      SUM(FactProductMetrics[certified_range_km]),
      BLANK()
  )
  ```
- **Return Type**: Decimal (`0.0` Wh/km)
- **Business Purpose**: Aggregate energy consumption rate across catalog models.

---

## 5. Market Positioning & Segmentation Measures (Verified)

### 5.1 `[Budget Product Count]`
- **DAX Formula**:
  ```dax
  Budget Product Count = 
  CALCULATE(
      COUNTROWS(FactProductMetrics),
      FILTER(
          ProductPositioning,
          ProductPositioning[price_bucket] = "budget"
      )
  )
  ```
- **Return Type**: Whole Number
- **Business Purpose**: Count of commuter models priced under ₹100,000 (3 models).

### 5.2 `[Mid-Market Product Count]`
- **DAX Formula**:
  ```dax
  Mid-Market Product Count = 
  CALCULATE(
      COUNTROWS(FactProductMetrics),
      FILTER(
          ProductPositioning,
          ProductPositioning[price_bucket] = "mid-market"
      )
  )
  ```
- **Return Type**: Whole Number
- **Business Purpose**: Count of mainstream adoption models priced ₹100k–₹180k (19 models).

### 5.3 `[Premium Product Count]`
- **DAX Formula**:
  ```dax
  Premium Product Count = 
  CALCULATE(
      COUNTROWS(FactProductMetrics),
      FILTER(
          ProductPositioning,
          ProductPositioning[price_bucket] = "premium"
      )
  )
  ```
- **Return Type**: Whole Number
- **Business Purpose**: Count of luxury/flagship models priced above ₹180,000 (0 verified models; ceiling is ₹170k).

### 5.4 `[Long-Range Product Count]`
- **DAX Formula**:
  ```dax
  Long-Range Product Count = 
  CALCULATE(
      COUNTROWS(FactProductMetrics),
      FILTER(
          ProductPositioning,
          ProductPositioning[range_bucket] = "long-range"
      )
  )
  ```
- **Return Type**: Whole Number
- **Business Purpose**: Models with certified range > 180 km (4 models).

### 5.5 `[High-Performance Product Count]`
- **DAX Formula**:
  ```dax
  High-Performance Product Count = 
  CALCULATE(
      COUNTROWS(FactProductMetrics),
      FILTER(
          ProductPositioning,
          ProductPositioning[performance_bucket] = "high-performance"
      )
  )
  ```
- **Return Type**: Whole Number
- **Business Purpose**: Models with top speed > 90 km/h (7 models).

### 5.6 `[Products Above Market Average]` & `[Products Below Market Average]`
- **DAX Formula**:
  ```dax
  Products Above Market Average = 
  CALCULATE(
      COUNTROWS(FactProductMetrics),
      FILTER(
          PricingAnalysis,
          PricingAnalysis[relative_price_position] = "above market average"
      )
  )
  
  Products Below Market Average = 
  CALCULATE(
      COUNTROWS(FactProductMetrics),
      FILTER(
          PricingAnalysis,
          PricingAnalysis[relative_price_position] = "below market average"
      )
  )
  ```
- **Return Type**: Whole Number
- **Business Purpose**: Quantifies skew of catalog pricing relative to the arithmetic mean.

### 5.7 `[Product Portfolio HHI]`
- **DAX Formula**:
  ```dax
  Product Portfolio HHI = 
  VAR TotalCount = CALCULATE(COUNTROWS(FactProductMetrics), ALL(DimManufacturer))
  RETURN
  SUMX(
      DimManufacturer,
      POWER(
          DIVIDE(CALCULATE(COUNTROWS(FactProductMetrics)), TotalCount, 0) * 100.0,
          2
      )
  )
  ```
- **Return Type**: Decimal (`#,##0.0`)
- **Business Purpose**: Quantifies product offering concentration across OEMs (HHI = 2,333.3).

---

## 6. Pending Market Registration DAX Measures (Fail-Closed)

In strict adherence to the project's **provenance safeguard**, these measures return `BLANK()` to prevent proxy figures from masquerading as factual dashboard data:

```dax
Total EV Registrations (Pending) = BLANK()
YoY Market Growth Pct (Pending) = BLANK()
Market CAGR Pct (Pending) = BLANK()
EV Penetration Pct (Pending) = BLANK()
OEM Registration Market Share Pct (Pending) = BLANK()
Market Volume HHI (Pending) = BLANK()
State Registration Rank (Pending) = BLANK()
Market Intelligence Data Status = "PENDING VERIFIED VAHAN DATA"
```

---

## 7. DAX Validation & Execution Limitations

- **Validation Status**: **DAX authored and statically verified, but not executed in Power BI Desktop.**
- **Environment Audit**: Power BI Desktop (`PBIDesktop.exe`) was audited on the local Windows system and confirmed **not installed**.
- **Static Verification**: All 24 DAX measures were verified for balanced parentheses, proper function signatures (`CALCULATE`, `DIVIDE`, `DISTINCTCOUNT`, `FILTER`, `ALL`, `SUMX`, `POWER`), and schema alignment against `FactProductMetrics`, `DimManufacturer`, `DimProduct`, `PricingAnalysis`, and `ProductPositioning`.
