# Data Acquisition Guide — Indian EV 2-Wheeler Market Registrations

**Project**: Market-Business-Strategy-Intelligence  
**Governance**: Strict Anti-Fabrication Mandate & CERT-In Compliance  
**Last Updated**: 2026-09-12  

---

## 1. Purpose & Guiding Principles

This guide details legitimate, compliant procedures for human operators to extract official Indian Electric Two-Wheeler (e2W) registration data from government portals. 

### Core Ethical & Technical Safeguards
- **Zero-Bypass Policy**: Do NOT use automated CAPTCHA solvers, headless browser scrapers, or session forgery tools.
- **Official Portals Only**: Only primary sources (MoRTH Vahan, Open Government Data Platform, SEBI filings) are accepted.
- **Fail-Closed Governance**: Until data extracted via these steps is loaded and verified, all downstream reporting components (DuckDB marts, DAX measures) remain in fail-closed (`BLANK()` / empty) status.

---

## 2. Route A: MoRTH Vahan 4.0 Public Dashboard (Manual Extraction)

The Ministry of Road Transport & Highways (MoRTH) operates the Vahan 4.0 national vehicle registry analytics dashboard.

### Step-by-Step Retrieval Procedure

1. **Navigate to Dashboard**:
   - Access URL: `https://vahan.parivahan.gov.in/vahan4dashboard/` or `https://analytics.parivahan.gov.in/analytics/publicdashboard/vahan`
2. **Select Report Type**:
   - In the left navigation, select **"Vehicle Class & Fuel Type"** or **"Maker & Fuel Type"**.
3. **Configure Filter Parameters**:
   - **Fuel**: Select `ELECTRIC(BOV)` (Battery Operated Vehicle).
   - **Vehicle Category**: Select `2 WHEELER` or `TWO WHEELER (NT)` (Non-Transport).
   - **Y-Axis / Group By**: Select `State` or `Maker` (depending on analysis target).
   - **X-Axis**: Select `Year` or `Month`.
4. **Select Date Window**:
   - *Note*: The portal limits queries to a **1-year window** per report.
   - Query each year individually from 2014 through 2025 (12 queries).
5. **Solve Security Challenge**:
   - Enter the graphical CAPTCHA displayed on screen.
6. **Export Data**:
   - Click the export button (Excel/CSV icon) or copy the verified table.
7. **Deposit into Repository**:
   - Save the unedited file into:
     ```text
     data/raw/market_registrations/vahan/vahan_e2w_registrations_<YEAR>.xlsx
     ```
8. **Record Ingestion Metadata**:
   - Note retrieval timestamp, operator name, and portal URL in `docs/DATA_SOURCE_REGISTER.md`.

---

## 3. Route B: Open Government Data (OGD) Platform India (`data.gov.in`)

The Government of India provides open datasets via the Open Government Data (OGD) portal with an official REST API.

### Step-by-Step Retrieval Procedure

1. **Register for an API Key**:
   - Navigate to `https://data.gov.in/`.
   - Create a free developer account and obtain a unique API key.
2. **Locate Target EV Dataset**:
   - Search for: *"State-wise Registration of Electric Vehicles"* or Ministry of Heavy Industries FAME / PM E-DRIVE release catalogs.
   - Resource ID example: `93d9e76e-c7d0-4e81-9c87-97543b5d2a36`
3. **Execute API Query**:
   ```bash
   curl -X GET "https://api.data.gov.in/resource/<RESOURCE_ID>?api-key=<YOUR_API_KEY>&format=csv&limit=10000" -o data/raw/market_registrations/vahan/ogd_ev_registrations_raw.csv
   ```
4. **Validate Response**:
   - Verify HTTP status code 200.
   - Check headers for proper CSV content type.
   - Inspect whether vehicle class (2W) is explicitly disaggregated.

---

## 4. Route C: SEBI Regulatory Filings & OEM Annual Reports (OEM-Level Volumes)

For verified manufacturer-level volumes:

1. **Ola Electric Mobility Limited**:
   - Document: SEBI Red Herring Prospectus (DRHP / RHP 2024).
   - Section: *"Industry Overview"* & *"Our Business"*.
   - Data captured: Annual e2W industry registration totals and OEM volumes (FY2021–FY2024).
2. **TVS Motor Company & Bajaj Auto Limited**:
   - Document: Annual Reports (Business Responsibility & Sustainability Reports / Management Discussion).
   - Section: Electric vehicle dispatch / registration disclosures.

---

## 5. Post-Ingestion Processing Pipeline

Once raw data files are deposited into `data/raw/market_registrations/vahan/`:

```bash
# 1. Run normalization and schema validation
python src/market_data_ingestion.py

# 2. Run SQL warehouse pipeline to populate marts
python src/run_sql_pipeline.py

# 3. Validate PBIP and DAX measures
python powerbi/validate_pbip.py

# 4. Run test suite
python -m pytest -v
```
