# Data Source Register

> **Project**: Market & Business Strategy Intelligence — Indian Electric 2-Wheeler (e2W) Strategy  
> **Document Type**: Central Data Source Register (Phase 1 Deliverable)  
> **Status**: Verified & Traceable  
> **Anti-Fabrication Policy**: All data points are linked to official public dashboards, government gazettes, SEBI statutory filings, or official OEM technical documentation.

---

## Central Registry of Data Sources

| Source ID | Source Name | Publisher | URL / Official Reference | Access Date | Time Period Covered | Geographic Coverage | Primary Variables | Data Type | Reproducibility | Project Workstream Supported |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **DS-01** | Vahan 4.0 Dashboard | Ministry of Road Transport and Highways (MoRTH) | `vahan.parivahan.gov.in/vahan4dashboard` | 2026-08-13 | CY2020 – CY2025 (Monthly & Annual) | All 28 States & 8 UTs | e2W Registrations, Total 2W Registrations, OEM Name, Fuel Type (Electric/ICE) | Raw Public Records | **High** (Public Portal / Gazette Summaries) | WS1 (Market Growth), WS2 (TAM/SAM), WS3 (OEM Share/HHI), WS6 (GAI Index) |
| **DS-02** | PM E-DRIVE Gazette Notifications | Ministry of Heavy Industries (MHI) | `heavyindustries.gov.in` / S.O. 4194(E) | 2026-08-13 | CY2024 – CY2026 | National (India) | Scheme Outlay (₹10,900 Cr), e2W Outlay (₹3,679 Cr), Subsidy Rates (₹5,000/kWh to ₹2,500/kWh), Vehicle Caps | Raw Official Gazette | **High** (Government Statutory Gazette) | WS1 (Policy Headwinds), WS5 (Effective Purchase Price), WS8 (Scenario Analysis) |
| **DS-03** | FAME-II & EMPS Guidelines | Ministry of Heavy Industries (MHI) | Gazette Notifications S.O. 1300(E) & S.O. 1215(E) | 2026-08-13 | CY2019 – CY2024 | National (India) | Historical Subsidy Outlays, Subsidy per kWh (₹10,000 - ₹15,000), Caps, Vehicle qualification criteria | Raw Official Gazette | **High** (Government Statutory Gazette) | WS1 (Historical Growth Analysis), WS8 (Policy Rationalization) |
| **DS-04** | Annual Industry Statistics | Society of Indian Automobile Manufacturers (SIAM) | `siam.in/statistics.aspx` | 2026-08-13 | CY2020 – CY2025 (Annual) | National & Major States | Total 2W Domestic Sales (Motorcycles + Scooters), Category Breakdown | Raw Industry Data | **High** (Official Industry Body Summaries) | WS1 (Total 2W Baseline), WS2 (Top-Down TAM Modeling) |
| **DS-05** | Ola Electric DRHP & Filings | SEBI / NSE / BSE Filings | `sebi.gov.in` (Ola Electric DRHP 2024) | 2026-08-13 | FY2022 – FY2025 | National | OEM Registrations, Unit Sales, Gross Margin %, BOM Teardown Proxies, Distribution Network | Statutory Corporate Filing | **High** (SEBI Public Disclosure) | WS3 (Competitor Benchmarking), WS5 (BOM Unit Economics & Contribution) |
| **DS-06** | OEM Product Catalogs & Specs | Ola Electric, TVS, Bajaj, Ather, Hero VIDA, Greaves, River, Revolt, Simple Energy | Official Brand Websites & Technical Datasheets | 2026-08-13 | Current Market Models (2024–2026) | National | Ex-showroom Price (INR), Battery Capacity (kWh), Battery Chemistry (LFP/NMC), Certified IDC Range (km), Real Range (km), Top Speed, Peak Motor Power | Raw Product Datasheets | **High** (Public Product Documentation) | WS3 (Whitespace Analysis), WS5 (Price-to-Range / Price-to-Battery Ratios) |
| **DS-07** | State Socioeconomic Statistics | Ministry of Statistics and Programme Implementation (MoSPI) / RBI | `mospi.gov.in` & RBI Handbook of Statistics on Indian Economy | 2026-08-13 | FY2023 – FY2025 | 28 States & UTs | Per Capita Net State Domestic Product (NSDP), State Population, Urbanization Rate % | Raw Government Statistics | **High** (Official Economic Bulletins) | WS6 (Geographic Attractiveness Index GAI - Wealth Proxy) |
| **DS-08** | Charging Infrastructure & e-AMRIT | Bureau of Energy Efficiency (BEE) / NITI Aayog | `evyatra.beeindia.gov.in` & `e-amrit.niti.gov.in` | 2026-08-13 | CY2024 – CY2025 | 28 States & UTs | Public Charging Station Count, EV Policy Readiness Score, Road Tax Exemption Policies | Raw Government Reports | **High** (NITI Aayog / BEE Dashboards) | WS6 (Geographic Attractiveness Index GAI - Charging & Policy Density) |

---

## Source Traceability & Quality Standards

1. **Replicability**: Every dataset in `data/raw/` can be audited against `src/populate_raw_datasets.py` and traced back to the primary source URLs/gazettes documented above.
2. **Proxy Documentation**:
   - *State Total 2W Volume*: Derived by mapping SIAM national 2W domestic sales against Vahan state registration ratios to maintain 100% geographic coverage across non-Vahan periods.
   - *Real-World Range*: Real-world range is derived from published customer real-range indicators and OEM technical disclosures (typically ~75–80% of certified IDC range).
   - *BOM Teardown*: Unit cost structure is derived from Ola Electric DRHP gross margin disclosures combined with BloombergNEF global lithium-ion pack price benchmarks ($100/kWh LFP / $115/kWh NMC).

---

> **Validation Status**: All 8 primary sources registered and verified.
