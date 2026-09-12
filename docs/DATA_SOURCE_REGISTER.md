# Data Source Register

Audit date: 2026-09-07. Source classifications below control analytical eligibility in the pipeline.

| Dataset | Status | Source | Coverage | Retrieval/export availability | Limitations |
|---|---|---|---|---|---|
| `verified_product_catalog_2025_2026.csv` | Verified primary-source | Official TVS, Chetak/Bajaj, Ola, Ather, and Ampere pages, brochures and releases. Per-row URLs retained. | 30 variants, 5 manufacturers, 2025-2026 launch/current information, India | Source URLs and access date retained per row | Prices vary by city, incentive and offer date. Blank field means the cited source did not support it. |
| `vahan_e2w_registrations_monthly.csv` | Proxy/deprecated | Legacy claimed Vahan. [Vahan dashboard](https://analytics.parivahan.gov.in/analytics/publicdashboard/vahan) | 2020-2025, 19 jurisdictions | Not a downloaded export | Generated from fixed shares and seasonality. Never use as observed registrations. |
| `oem_e2w_registrations_annual.csv` | Proxy/deprecated | Legacy claimed Vahan/Ola DRHP | 2020-2025, India | No retained extract | Manual/generated values. Market shares and HHI are non-factual derived outputs. |
| `competitor_product_catalog.csv` | Unverified legacy | Legacy manual compilation | 31 rows, undated | No per-row URL/access date | Superseded for verified use by the verified catalog. |
| `state_socioeconomic_indicators.csv` | Proxy/deprecated | Legacy claimed MoSPI/RBI/BEE | 20 jurisdictions, undated | No retained extract | Includes estimated 2W volume and support score. Do not use for state analysis. |
| `policy_incentive_timeline.csv` | Unverified transcription | [MHI notifications](https://heavyindustries.gov.in/en/notifications-archives), [PM E-DRIVE guidelines](https://heavyindustries.gov.in/en/scheme-guidelines), [FAME-II notification](https://heavyindustries.gov.in/sites/default/files/2023-09/2-notification.pdf) | 2019-2026, India | Links retained; PDFs/extraction notes absent | Verify every value and amendment before use. |

## Registration-data acquisition finding

The official [Vahan public dashboard](https://analytics.parivahan.gov.in/analytics/publicdashboard/vahan) exposes state, maker, fuel, class, monthly/yearly filters and a 15-year trend. The official [Vahan tabular report](https://analytics.parivahan.gov.in/analytics/vahanpublicreport?lang=en) requires a CAPTCHA and allows a maximum one-year date range. No CAPTCHA was bypassed and no chart values were reconstructed. To obtain factual e2W data, manually export each one-year report with documented electric-two-wheeler filters, preserve the untouched export, and record retrieval date and filter definitions.

The Government OGD catalog describes a State/UT total-EV Vahan4 resource for 2020-2023, but it does not provide the e2W/month/OEM detail required here. SIAM provides state/model and monthly sales products, but the relevant detailed files are commercial rather than a freely downloadable official source.
