# Data Source Register & Provenance Audit

Audit Date: 2026-09-12  
Governance Authority: Market & Business Strategy Intelligence Provenance Standards

---

## 1. Primary Source Inventory & Classification Matrix

| Dataset Identifier | File Path | Provenance Class | Verification Status | Eligible as Observed Analytics | Publisher / Primary Source | Coverage | Limitations / Retrieval Notes |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- | :--- |
| **`verified_product_catalog_2025_2026.csv`** | `data/raw/` & `data/processed/` | `verified_primary_source` | **VERIFIED** | **YES** | Official OEM portals, press releases, technical brochures, and SEBI IPO disclosures (TVS, Bajaj, Ola, Ather, Ampere, Hero VIDA, Simple Energy, Revolt Motors, Ultraviolette, Kinetic Green, BGauss). | 42 models across 11 manufacturers (2025–2026 models, India). | Prices are ex-showroom (location/offer specific). Blank values indicate source did not capture that parameter. |
| **`vahan_e2w_registrations_monthly.csv`** | `data/raw/` & `data/processed/` | `generated_proxy` | **PROXY_DEPRECATED** | **NO** | Legacy simulator claiming MoRTH Vahan 4.0. | 2020–2025, 19 Indian states/UTs. | **Not an official download.** Generated from assumed seasonality and fixed state allocations. Prohibited from factual reporting. |
| **`oem_e2w_registrations_annual.csv`** | `data/raw/` & `data/processed/` | `generated_proxy` | **PROXY_DEPRECATED** | **NO** | Legacy simulator claiming Vahan & Ola DRHP. | 2020–2025, annual OEM totals. | Rounded annual estimates without row-level extraction trace. Prohibited from factual reporting. |
| **`state_socioeconomic_indicators.csv`** | `data/raw/` & `data/processed/` | `generated_proxy` | **PROXY_DEPRECATED** | **NO** | Claimed MoSPI, RBI, BEE data. | 20 states/UTs. | Contains synthesized 2W volume and policy scoring. Used only as a structural scenario template. |
| **`policy_incentive_timeline.csv`** | `data/raw/` & `data/processed/` | `source_transcription_pending_document` | **PENDING_DOCUMENT_VERIFICATION** | **NO** | Ministry of Heavy Industries notifications (FAME-I, FAME-II, EMPS 2024, PM E-DRIVE). | 2015–2026 timeline. | Key policy dates captured, but formal gazette PDFs are not stored locally. |
| **`competitor_product_catalog.csv`** | `data/raw/` | `manual_compilation_unverified` | **UNVERIFIED_LEGACY** | **NO** | Legacy manual compilation (undated). | 31 models. | **Superseded** by `verified_product_catalog_2025_2026.csv`. |

---

## 2. Official Vahan / MoRTH Registration Data Acquisition Finding

An extensive audit was performed across official Government of India vehicle registration portals:

### 2.1 MoRTH Vahan 4.0 Public Dashboard (`analytics.parivahan.gov.in`)
- **Dashboard URL**: `https://analytics.parivahan.gov.in/analytics/publicdashboard/vahan`
- **Capabilities**: Exposes dynamic visualizations for vehicle category, fuel type (Electric), maker, and state-level registration counts.
- **Export & Automation Constraints**:
  - The underlying public analytics portal is protected by mandatory graphical **CAPTCHAs** for all tabular data generation endpoints (`/analytics/vahanpublicreport`).
  - Queries in the tabular report interface are hard-restricted to a **maximum 1-year date range** per query.
  - Automated web scraping, headless browser automation, or endpoint reverse engineering to bypass authentication or CAPTCHAs is **strictly prohibited by policy** and the Computer Emergency Response Team (CERT-In) guidelines.
  - No single bulk multi-year (10+ year) CSV download is provided via open API.

### 2.2 Open Government Data (OGD) Platform India (`data.gov.in`)
- **Portal**: Open Government Data Platform India.
- **Audit Finding**: OGD catalogs feature total EV registrations aggregated annually by State/UT for 2020–2023, but do not provide the granular vehicle class breakdown (specifically isolating two-wheelers from three-wheelers and commercial vehicles) or maker-level distribution required for factual e2W competitive share modeling.

### 2.3 Society of Indian Automobile Manufacturers (SIAM)
- **Portal**: SIAM Industry Statistics.
- **Audit Finding**: Monthly and annual dispatch/sales data by segment and maker is proprietary and sold under commercial subscription licenses rather than accessible as a public government open dataset.

---

## 3. Governance Policy: Fail-Closed Isolation

Because authoritative, row-level 10-year Vahan e2W registration series are not available locally without manual portal extraction:
1. The repository enforces **Fail-Closed Isolation**.
2. `pending.fact_ev_registrations` in DuckDB is maintained with **0 rows**.
3. All DAX measures for registration volumes return **`BLANK()`**.
4. Analytical models (YoY growth, CAGR, HHI, GAI) are fully implemented as mathematical functions and SQL query templates ready to execute immediately upon verified data ingestion.
5. No proxy dataset is ever relabeled or presented as official Vahan registrations.
