# Data Source Register & Provenance Audit

**Audit Date**: 2026-09-12 / 2026-09-13  
**Governance Authority**: Market & Business Strategy Intelligence Provenance Standards  
**Policy**: Strict Anti-Fabrication & Empirical Verification Standard  

---

## 1. Primary Source Inventory & Classification Matrix

| Dataset Identifier | File Path | Provenance Class | Verification Status | Eligible as Observed Analytics | Publisher / Primary Source | Coverage | Limitations / Retrieval Notes |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- | :--- |
| **`verified_product_catalog_2025_2026.csv`** | `data/raw/` & `data/processed/` | `verified_primary_source` | **VERIFIED** | **YES** | Official OEM portals, press releases, technical brochures, and SEBI IPO disclosures (TVS, Bajaj, Ola, Ather, Ampere, Hero VIDA, Simple Energy, Revolt Motors, Ultraviolette, Kinetic Green, BGauss). | 42 models across 11 manufacturers (2025–2026 models, India). | Prices are ex-showroom (location/offer specific). Blank values indicate source did not capture that parameter. |
| **`data/raw/market_registrations/vahan/`** | `data/raw/market_registrations/` | `verified_primary_source` | **AWAITING_INGESTION** | **YES (when loaded)** | Official MoRTH Vahan 4.0 Dashboard / data.gov.in extracts via `DATA_ACQUISITION_GUIDE.md`. | Target: 2014–2025, 20+ States/UTs, e2W segment. | Human operator manual extraction required due to portal CAPTCHA and 1-year date window query limits. |
| **`vahan_e2w_registrations_monthly.csv`** | `data/raw/` & `data/processed/` | `generated_proxy` | **PROXY_DEPRECATED** | **NO** | Legacy simulator claiming MoRTH Vahan 4.0. | 2020–2025, 19 Indian states/UTs. | **Not an official download.** Generated from assumed seasonality and fixed state allocations. Quarantined from factual reporting. |
| **`oem_e2w_registrations_annual.csv`** | `data/raw/` & `data/processed/` | `generated_proxy` | **PROXY_DEPRECATED** | **NO** | Legacy simulator claiming Vahan & Ola DRHP. | 2020–2025, annual OEM totals. | Rounded annual estimates without row-level extraction trace. Quarantined from factual reporting. |
| **`state_socioeconomic_indicators.csv`** | `data/raw/` & `data/processed/` | `generated_proxy` | **PROXY_DEPRECATED** | **NO** | Claimed MoSPI, RBI, BEE data. | 20 states/UTs. | Contains synthesized 2W volume and policy scoring. Used only as a structural scenario template. |
| **`policy_incentive_timeline.csv`** | `data/raw/` & `data/processed/` | `source_transcription_pending_document` | **PENDING_DOCUMENT_VERIFICATION** | **NO** | Ministry of Heavy Industries notifications (FAME-I, FAME-II, EMPS 2024, PM E-DRIVE). | 2015–2026 timeline. | Key policy dates captured, but formal gazette PDFs are not stored locally. |
| **`competitor_product_catalog.csv`** | `data/raw/` | `manual_compilation_unverified` | **UNVERIFIED_LEGACY** | **NO** | Legacy manual compilation (undated). | 31 models. | **Superseded** by `verified_product_catalog_2025_2026.csv`. |

---

## 2. Official Primary Source Investigation Results (Phase 2–3 Audit)

An exhaustive investigation across seven potential primary sources was completed in September 2026:

### 2.1 MoRTH Vahan 4.0 Public Dashboard (`analytics.parivahan.gov.in`)
- **Dashboard URL**: `https://analytics.parivahan.gov.in/analytics/publicdashboard/vahan`
- **Capabilities**: Contains genuine national registration records from 2003 to 2026 for all 36 States/UTs, disaggregable by vehicle class (`2 WHEELER`), fuel (`ELECTRIC(BOV)`), and maker.
- **Access Barriers**:
  - Mandatory client-side graphical CAPTCHA for all tabular data generation endpoints (`/analytics/vahanpublicreport`).
  - Strict 365-day query boundary per request.
  - Automated bypass prohibited by CERT-In security policies and portal Terms of Service.
- **Status**: Data exists; legitimate acquisition requires manual query-by-query export by human operator as documented in `docs/DATA_ACQUISITION_GUIDE.md`.

### 2.2 Open Government Data (OGD) Platform India (`data.gov.in`)
- **API Endpoint**: `https://api.data.gov.in/resource/`
- **Catalog Evaluated**: *"State-wise Registration of Electric Vehicles"*
- **Access Barriers**:
  - Web portal renders as a dynamic JavaScript Single Page Application without raw HTML tables.
  - REST API gateway enforces authentication via unique user API keys (HTTP 403 when unauthenticated).
  - Public national datasets do not isolate the two-wheeler category from commercial and 3-wheeler EVs.
- **Status**: Free registration required to obtain API key; category filters need supplementary reconciliation.

### 2.3 Ministry of Heavy Industries (MHI)
- **Endpoints**: `heavyindustries.gov.in/en/page/ev-sales`
- **Status**: Returned HTTP 404 (Not Found). Historical multi-year national time series are not published as machine-readable open tables on MHI web pages.

### 2.4 MoRTH Transport Research Wing (Road Transport Year Book)
- **Endpoints**: `morth.nic.in/road-transport-year-book`
- **Status**: Connection timed out / unreachable during audit.

### 2.5 Society of Indian Automobile Manufacturers (SIAM)
- **Portal**: `siam.in`
- **Status**: Commercial proprietary source. Sales and dispatch statistics are gated behind paid enterprise subscriptions and unavailable as public open data.

### 2.6 Ola Electric SEBI Red Herring Prospectus (DRHP / RHP 2024)
- **Authority**: Statutory public disclosure under SEBI ICDR Regulations.
- **Verified Data**: Discloses annual Indian E2W industry registration totals:
  - FY2021: ~41,000 units
  - FY2022: ~249,000 units
  - FY2023: ~728,000 units
  - FY2024: ~944,000 units
- **Limitation**: Covers only 4 fiscal years (national totals); does not provide 10+ year time-series or 20+ state granular panels.

---

## 3. Governance Policy: Fail-Closed Isolation

Because authoritative, row-level 10-year Vahan e2W registration series are not available locally without manual portal extraction:
1. The repository enforces **Fail-Closed Isolation**.
2. `pending.fact_ev_registrations` in DuckDB is maintained with **0 rows**.
3. All DAX measures for registration volumes return **`BLANK()`**.
4. Analytical models (YoY growth, CAGR, HHI, GAI) are fully implemented as mathematical functions and SQL query templates ready to execute immediately upon verified data ingestion.
5. No proxy dataset is ever relabeled or presented as official Vahan registrations.
