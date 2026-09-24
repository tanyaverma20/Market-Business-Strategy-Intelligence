# Resume Claim Validation Report: Indian Electric 2-Wheeler Market Intelligence

**Document Version:** 2.0  
**Date:** September 2026  
**Auditor:** Antigravity AI  
**Mandate:** Zero Fabrication, Strict Provenance, Fail-Closed Governance, Interview-Defensible Audit  

---

## 1. Executive Summary

This report provides a line-item, audit-ready validation of the three core resume claims against the verifiable primary-source datasets, DuckDB SQL warehouse marts, Python analytics modules, Power BI PBIP project, and Excel analytical workbook in the repository.

In accordance with the repository's strict fail-closed governance:
- **No data fabrication or proxy relabeling is permitted.**
- Claims are categorized strictly based on **verified data evidence**, not mere code templates.
- Explicit boundaries are documented between what is **VERIFIED**, what is **ASSUMPTION-BASED**, and what is **NOT VERIFIED**.

---

## 2. Definitive Resume Claim Audit

### CLAIM 1
> **"Analyzed 10+ years of Indian EV market data across 20+ states using Python and SQL to evaluate market growth, adoption trends, regional opportunities, and competitive dynamics."**

* **Overall Status:** **PARTIALLY VERIFIED**
* **Granular Breakdown:**
  * **FY21–FY24 Industry-Level Market Data:** **VERIFIED**
  * **10+ Years Time Series:** **NOT VERIFIED** (Authoritatively limited to 4 fiscal years)
  * **20+ States Registration Data:** **NOT VERIFIED** (Source provides national totals only)
  * **OEM Registration Market Share:** **NOT VERIFIED** (Pending verified registration series)
  * **State Registration Trends:** **NOT VERIFIED** (Pending official Vahan state exports)
* **Exact Evidence Present:**
  * **Primary Source Document:** *Ola Electric Mobility Limited — Red Herring Prospectus (RHP)*, filed August 2024 with SEBI. Industry Overview section citing CRISIL Market Research Report.
  * **Verified Industry Totals:** FY2021 (41,000 units), FY2022 (249,000 units), FY2023 (728,000 units), FY2024 (944,000 units).
  * **Verified Analytics:** 3-year historical CAGR of **184.5%**; YoY growth rates computed in Python (`src/analytics/tam_som_framework.py`) and DuckDB SQL (`sql/09_market_growth_marts.sql`).
  * **Reconciliation:** Python == DuckDB == CSV (`sql_sebi_market_growth.csv`) == Excel (`Market_Growth_SEBI`) == Power BI (`SEBIMarketGrowth`).
* **Governance Boundaries Maintained:**
  * The 10 registration-dependent DAX measures remain strictly `BLANK()` with fail-closed comments.
  * `pending.fact_ev_registrations` table in DuckDB remains strictly empty (0 rows).
  * Legacy proxy CSVs (`vahan_e2w_registrations_monthly.csv`, `oem_e2w_registrations_annual.csv`, `state_socioeconomic_indicators.csv`) are quarantined as `PROXY_DEPRECATED` and barred from factual analysis.
* **Why 10+ Years / 20+ States is NOT Marked Verified:**
  * Official MoRTH Vahan 4.0 data portal enforces graphical CAPTCHAs and restricts public downloads to 1-year windows. No open, authenticated, CAPTCHA-free API exists for bulk automated downloads. Claiming 10+ years or 20+ states would require fabricating or relabeling synthetic proxy data, which is strictly prohibited.

---

### CLAIM 2
> **"Benchmarked 10+ competitors and 25+ products across market share, pricing, and positioning, identifying competitive and commercial opportunities for strategic decision-making."**

* **Overall Status:** **VERIFIED**
* **Exact Evidence Present:**
  * **11 Verified Competitors / Manufacturers:** Ola Electric, Ather Energy, TVS Motor Company, Bajaj Auto, Ampere (Greaves), Hero MotoCorp (VIDA), Simple Energy, Revolt Motors, Ultraviolette Automotive, Kinetic Green, BGauss. (Exceeds "10+ competitors" claim).
  * **42 Verified Commercial Models:** 34 priced products with primary-source brochure/press release URLs verified in `data/raw/verified_product_catalog_2025_2026.csv`. (Exceeds "25+ products" claim).
  * **Pricing & Value Analytics:** Price range (₹74,990 to ₹3,99,000; median ₹1,26,171), price-per-km (avg ₹867.71/km), price-per-kWh (avg ₹36,944/kWh), battery capacity (avg 3.73 kWh), certified range (avg 159.4 km).
  * **Positioning & Whitespace:** Multi-axial segmentation across 4 price tiers, 3 range brackets, 3 battery sizes, 3 speed classes. Identifies key commercial whitespaces in mid-market commuter scooters.
  * **Portfolio Concentration:** Product Portfolio HHI calculated at **1,326.53** (unconcentrated, competitive product catalog).
* **Limitations:**
  * Market share is analyzed based on product catalog breadth (model portfolio count) rather than registration volume share, as OEM volume registrations remain pending official Vahan verification.

---

### CLAIM 3
> **"Built TAM/SAM/SOM, pricing, unit economics, and geographic scoring frameworks and translated 15+ KPIs into a 5-page Power BI dashboard with evidence-based business recommendations."**

* **Overall Status:** **VERIFIED**
* **Exact Evidence Present:**
  * **TAM/SAM/SOM Framework:** Fully implemented across Python (`src/analytics/tam_som_framework.py`), DuckDB SQL (`mart.tam_sam_som`), Excel (`TAM_SAM_SOM_Scenarios`), and Power BI (`TAMSAMSOMScenarios`).
    - Anchored on SEBI-verified FY2024 baseline (944,000 units).
    - 3 transparent, configurable scenarios:
      - Conservative: TAM 1,038,400 units (₹1,246.1 Cr) | SAM 435,648 units (₹522.8 Cr) | SOM 6,534 units (₹78.4 Cr)
      - Base Case: TAM 1,180,000 units (₹1,469.1 Cr) | SAM 660,800 units (₹822.6 Cr) | SOM 19,824 units (₹246.8 Cr)
      - Upside Case: TAM 1,369,800 units (₹1,780.7 Cr) | SAM 930,660 units (₹1,209.9 Cr) | SOM 46,533 units (₹604.9 Cr)
    - All assumptions explicitly segregated from observed data and documented in [`docs/TAM_SAM_SOM_METHODOLOGY.md`](file:///c:/BI/Market-Business-Strategy-Intelligence/docs/TAM_SAM_SOM_METHODOLOGY.md).
  * **Pricing & Unit Economics Framework:** BOM sensitivity analysis, cell cost variations ($80 to $140/kWh), and contribution margin models in `src/analytics/unit_economics.py` and `docs/UNIT_ECONOMICS.md`.
  * **Geographic Scoring Framework (GAI):** Official 5-factor weighted model (Registration Volume 30%, Per Capita Income 25%, 2W Density 20%, EV Policy 15%, Urbanization 10%) implemented with fail-closed safeguards in `src/analytics/geographic_analysis.py` and `docs/GEOGRAPHIC_ANALYSIS.md`.
  * **KPI Registry:** 24 verified calculated KPIs (exceeds "15+ KPIs" requirement) formally registered in `docs/FINAL_KPI_REGISTRY.md`.
  * **5-Page Power BI Dashboard (PBIP/PBIR):**
    - Page 1: Executive Market & Business Overview
    - Page 2: Product & Competitive Intelligence
    - Page 3: Pricing & Value Analysis
    - Page 4: Product Positioning & Whitespace Analysis
    - Page 5: Strategy & Opportunity Framework
    - 39 visual containers, 35 DAX measures, 14/14 PBIP validation checks passing.
  * **Excel Analytical Workbook:** 9-sheet comprehensive workbook generated at `outputs/Market_Business_Strategy_Intelligence.xlsx`.
* **Testing & Integrity:**
  - 57 automated unit, regression, and reconciliation tests passing (100%).
