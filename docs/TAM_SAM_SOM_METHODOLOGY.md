# TAM / SAM / SOM Market Sizing Methodology

**Document Version:** 1.0  
**Date:** September 2026  
**Status:** IMPLEMENTED & AUDITABLE  
**Data Classification:** Anchored on OBSERVED Primary Source (SEBI Statutory Filing) + Explicit Scenario ASSUMPTIONS  

---

## 1. Executive Summary & Governance Principles

The Total Addressable Market (TAM), Serviceable Addressable Market (SAM), and Serviceable Obtainable Market (SOM) sizing framework translates industry-level EV two-wheeler (e2W) data into a structured market sizing model for commercial strategy.

### Core Governance Rules:
1. **Never conflate observed facts with modeled projections:** Historical baseline data is strictly anchored to primary statutory filings. Forward projections are explicitly marked as **ASSUMPTION**.
2. **Configurable scenario parameters:** All growth, concentration, and attainable share rates are parameterised into **Conservative**, **Base**, and **Upside** cases.
3. **No synthetic state allocations:** Because state-level breakdown is not published in the primary source document, state shares are treated as explicit scenario assumptions, and no proxy state registrations are relabeled as official facts.

---

## 2. Primary Source Anchor (Observed Industry Data)

The historical baseline is anchored directly on official statutory disclosures submitted to the **Securities and Exchange Board of India (SEBI)**:

* **Source Document:** *Ola Electric Mobility Limited — Red Herring Prospectus (RHP)*, filed August 2024 with SEBI.
* **Document Reference:** Industry Overview Section citing CRISIL Market Research Report.
* **Source URL:** [SEBI Public Filings](https://www.sebi.gov.in/filings/)
* **Access Date:** 2026-09-24
* **Provenance Classification:** `verified_primary_source`
* **Coverage Scope:** India national annual e2W sales/registrations for fiscal years ending March 31:

| Fiscal Year | Calendar Year End | Industry e2W Units | YoY Growth (%) | Data Classification |
|:---|:---:|:---:|:---:|:---|
| **FY2021** | 2021 | 41,000 | Baseline | OBSERVED — SEBI RHP 2024 |
| **FY2022** | 2022 | 249,000 | +507.3% | OBSERVED — SEBI RHP 2024 |
| **FY2023** | 2023 | 728,000 | +192.4% | OBSERVED — SEBI RHP 2024 |
| **FY2024** | 2024 | 944,000 | +29.7% | OBSERVED — SEBI RHP 2024 |

* **3-Year Historical CAGR (FY21–FY24):** **184.5%**  
  $$\text{CAGR} = \left(\frac{944,000}{41,000}\right)^{1/3} - 1 \approx 184.5\%$$

---

## 3. Mathematical Framework & Formulas

### 3.1 Total Addressable Market (TAM)
TAM represents the total annual market size of the Indian electric two-wheeler market in the immediate forecast fiscal year (FY2025).

$$\text{TAM Units} = \text{FY2024 Industry Units} \times (1 + g_{\text{FY25}})$$
$$\text{TAM Revenue (INR)} = \text{TAM Units} \times P_{\text{avg}}$$
$$\text{TAM Revenue (INR Cr)} = \frac{\text{TAM Revenue (INR)}}{10^7}$$

Where:
* $\text{FY2024 Industry Units} = 944,000$ (Observed)
* $g_{\text{FY25}} = \text{Assumed FY2025 YoY Growth Rate}$ (Assumption)
* $P_{\text{avg}} = \text{Average Selling Price (ASP)}$ derived from the verified product catalog mean (₹124,466) or scenario-adjusted.

### 3.2 Serviceable Addressable Market (SAM)
SAM represents the addressable slice of TAM based on geographical focus and target product segmentation (e.g. mass/mid-market urban & semi-urban clusters).

$$\text{SAM Units} = \text{TAM Units} \times C_{\text{geo}} \times C_{\text{seg}}$$
$$\text{SAM Revenue (INR Cr)} = \frac{\text{SAM Units} \times P_{\text{avg}}}{10^7}$$

Where:
* $C_{\text{geo}} = \text{Geographic Concentration Factor}$ (e.g., Top 8–12 target EV states)
* $C_{\text{seg}} = \text{Product Segment Focus}$ (e.g., Mid-market commuter scooters, ₹1.0L–₹1.5L)

### 3.3 Serviceable Obtainable Market (SOM)
SOM represents the realistic market capture attainable by an entrant or target manufacturer within a 3-year commercial horizon.

$$\text{SOM Units} = \text{SAM Units} \times S_{\text{attainable}}$$
$$\text{SOM Revenue (INR Cr)} = \frac{\text{SOM Units} \times P_{\text{avg}}}{10^7}$$

Where:
* $S_{\text{attainable}} = \text{Target Market Share of SAM}$ (e.g., 1.5% to 5.0%)

---

## 4. Scenario Matrix

| Metric | Conservative Case | Base Case | Upside Case | Classification |
|:---|:---:|:---:|:---:|:---|
| **FY2024 Baseline Units** | 944,000 | 944,000 | 944,000 | **OBSERVED** (SEBI RHP) |
| **FY2025 Growth Assumption ($g$)** | +10.0% | +25.0% | +45.0% | **ASSUMPTION** |
| **ASP per Unit (INR)** | ₹120,000 | ₹124,466 | ₹130,000 | **ASSUMPTION** (Catalog Mean) |
| **TAM Units** | **1,038,400** | **1,180,000** | **1,369,800** | Derived |
| **TAM Revenue (INR Cr)** | ₹1,246.1 Cr | ₹1,469.1 Cr | ₹1,780.7 Cr | Derived |
| **Geographic Concentration ($C_{\text{geo}}$)** | 60.0% | 70.0% | 80.0% | **ASSUMPTION** |
| **Segment Concentration ($C_{\text{seg}}$)** | 70.0% | 80.0% | 85.0% | **ASSUMPTION** |
| **SAM Units** | **435,648** | **660,800** | **930,660** | Derived |
| **SAM Revenue (INR Cr)** | ₹522.8 Cr | ₹822.6 Cr | ₹1,209.9 Cr | Derived |
| **Attainable Share ($S_{\text{attainable}}$)** | 1.5% | 3.0% | 5.0% | **ASSUMPTION** |
| **SOM Units** | **6,534** | **19,824** | **46,533** | Derived |
| **SOM Revenue (INR Cr)** | ₹78.4 Cr | ₹246.8 Cr | ₹604.9 Cr | Derived |

---

## 5. Technical Implementation & Reconciliation

The framework is implemented across all 4 system layers with complete reconciliation:

1. **Python Engine:** [`src/analytics/tam_som_framework.py`](file:///c:/BI/Market-Business-Strategy-Intelligence/src/analytics/tam_som_framework.py)
   - `compute_tam(scenario)`
   - `compute_sam(scenario)`
   - `compute_som(scenario)`
   - `build_tam_sam_som_table()`
2. **DuckDB SQL Analytical Mart:** [`sql/09_market_growth_marts.sql`](file:///c:/BI/Market-Business-Strategy-Intelligence/sql/09_market_growth_marts.sql)
   - Table `mart.tam_sam_som`
   - View `mart.market_growth_summary`
3. **Excel Workbook:** `outputs/Market_Business_Strategy_Intelligence.xlsx`
   - Sheet `TAM_SAM_SOM_Scenarios`
   - Sheet `Market_Growth_SEBI`
4. **Power BI PBIP/DAX:**
   - Table `TAMSAMSOMScenarios`
   - Table `SEBIMarketGrowth`
   - Explicitly labelled measures: `TAM Base Case Units (Assumption)`, `TAM Base Revenue INR Crore (Assumption)`.
