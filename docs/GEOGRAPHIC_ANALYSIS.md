# Geographic Attractiveness Index (GAI) Framework

**Document Version:** 2.0  
**Date:** September 2026  
**Status:** IMPLEMENTED & FAIL-CLOSED  
**Data Governance:** Production Mathematical Engine + Fail-Closed Quality Gate  

---

## 1. Executive Summary & Objective

The Geographic Attractiveness Index (GAI) is a multi-criteria spatial decision framework designed to evaluate and prioritize Indian states and union territories for commercial EV two-wheeler expansion.

### Governance Directive:
* **Fail-Closed Gate:** Factual state rankings are computed **only** when all required inputs for a state are verified from authoritative primary sources.
* **No Synthetic Proxy Rankings:** In accordance with repository data integrity rules, unverified proxy indicators (`state_socioeconomic_indicators.csv`, `vahan_e2w_registrations_monthly.csv`) are strictly prohibited from generating factual state rankings.
* **Status Classification:** Until state-level registration series are directly exported from official Vahan APIs/gazettes, the registration volume component remains **PENDING VERIFIED DATA**.

---

## 2. 5-Factor Weighted Model Architecture

The official 5-factor model evaluates regional markets across commercial demand, purchasing power, vehicle base, regulatory support, and demographic density:

| Factor | Weight ($w_i$) | Analytical Rationale | Required Authoritative Source | Current Status |
|:---|:---:|:---|:---|:---:|
| **Registration Volume Score** | **30%** (0.30) | Direct historical EV absorption capacity | Official MoRTH Vahan 4.0 Dashboard | **PENDING** |
| **Per Capita Income Score** | **25%** (0.25) | Local purchasing power & discretionary income | RBI / MoSPI State Domestic Product | Pending Verification |
| **Two-Wheeler Density Score** | **20%** (0.20) | Immediate addressable vehicle fleet size | MoRTH Road Transport Yearbook | Pending Verification |
| **State EV Policy Score** | **15%** (0.15) | Subsidies, road tax waivers, and local incentives | State EV Gazette Notifications / NITI Aayog | Pending Verification |
| **Urbanization Score** | **10%** (0.10) | Commuter density & charging feasibility | Census of India / MoHUA | Pending Verification |
| **Total** | **100%** (1.00) | Full multi-criteria spatial framework | — | — |

---

## 3. Mathematical Formulation

### 3.1 Normalization (Min-Max Scaling)
To ensure dimensional comparability across differing units (e.g. INR per capita vs vehicle counts), every input metric $x_i$ is normalized to a $[0, 100]$ scale across all evaluated states $S$:

$$\text{Norm}(x_{i, s}) = \begin{cases} \frac{x_{i, s} - \min_{j \in S}(x_{i, j})}{\max_{j \in S}(x_{i, j}) - \min_{j \in S}(x_{i, j})} \times 100 & \text{if } \max \neq \min \\ 0.0 & \text{otherwise} \end{cases}$$

### 3.2 Composite Weighted Score
For any state $s$ having a complete set of validated inputs:

$$\text{GAI Score}_s = \sum_{i=1}^{5} w_i \times \text{Norm}(x_{i, s})$$

Where:
* $w = \{0.30, 0.25, 0.20, 0.15, 0.10\}$
* $\sum w_i = 1.00$

### 3.3 Priority Tiers
States with complete scores are classified into strategic rollout tiers:
* **High Priority:** $\text{GAI Score} \ge 80.0$
* **Medium Priority:** $60.0 \le \text{GAI Score} < 80.0$
* **Watch:** $40.0 \le \text{GAI Score} < 60.0$
* **Low Priority:** $\text{GAI Score} < 40.0$

### 3.4 Dense Ranking
$$\text{GAI Rank}_s = \text{Rank}(\text{GAI Score}_s, \text{descending, method='dense'})$$

---

## 4. Fail-Closed Safeguard Rules

If any required metric $x_{i, s}$ is null, missing, or marked unverified:
1. $\text{GAI Score}_s = \text{None}$ (or `BLANK()`)
2. $\text{GAI Rank}_s = \text{None}$ (no state rank is assigned)
3. $\text{Data Quality Status}_s = \text{"INCOMPLETE - Missing inputs: fail-closed"}$

This prevents misleading business decisions based on partial or proxy data.

---

## 5. Technical Implementation & Modules

* **Python Implementation:** [`src/analytics/geographic_analysis.py`](file:///c:/BI/Market-Business-Strategy-Intelligence/src/analytics/geographic_analysis.py)
  - `compute_gai_scores(df, weights)`: 5-factor model with fail-closed safeguards.
  - `compute_gai_template(df, weights)`: Compatibility template for testing.
  - `_safe_normalize(series)`: Vectorized min-max normalization.
* **Unit & Regression Tests:** [`src/tests/test_market_growth_tam_som.py`](file:///c:/BI/Market-Business-Strategy-Intelligence/src/tests/test_market_growth_tam_som.py)
  - `test_gai_5_factor_weights`
  - `test_gai_fail_closed_on_missing_column`
  - `test_gai_fail_closed_on_null_values`
  - `test_gai_complete_data_scores_and_ranks`
* **Excel Workbook Integration:** `outputs/Market_Business_Strategy_Intelligence.xlsx`
  - `Executive_KPI_Summary`: GAI Framework listed with governance disclaimer.
  - `Assumptions_Provenance`: Explicitly audits GAI dependencies.
