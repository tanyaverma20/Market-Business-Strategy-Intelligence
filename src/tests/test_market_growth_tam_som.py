from pathlib import Path
import pandas as pd
import pytest
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


@pytest.fixture(scope="module")
def tam_som_module():
    from analytics.tam_som_framework import (
        compute_tam, compute_sam, compute_som,
        build_tam_sam_som_table, build_sebi_market_growth_table,
        SEBI_VERIFIED_FY2024_INDUSTRY_UNITS, SEBI_VERIFIED_SOURCE,
    )
    return {
        "compute_tam": compute_tam, "compute_sam": compute_sam, "compute_som": compute_som,
        "build_tam_sam_som_table": build_tam_sam_som_table,
        "build_sebi_market_growth_table": build_sebi_market_growth_table,
        "SEBI_VERIFIED_FY2024_INDUSTRY_UNITS": SEBI_VERIFIED_FY2024_INDUSTRY_UNITS,
        "SEBI_VERIFIED_SOURCE": SEBI_VERIFIED_SOURCE,
    }


class TestSEBIMarketGrowth:
    def test_sebi_data_has_four_verified_years(self, tam_som_module):
        df = tam_som_module["build_sebi_market_growth_table"]()
        assert len(df) == 4
        assert set(df["fiscal_year"]) == {"FY2021", "FY2022", "FY2023", "FY2024"}

    def test_sebi_industry_totals_match_rhp(self, tam_som_module):
        df = tam_som_module["build_sebi_market_growth_table"]()
        totals = dict(zip(df["fiscal_year"], df["industry_e2w_units"]))
        assert totals["FY2021"] == 41000
        assert totals["FY2022"] == 249000
        assert totals["FY2023"] == 728000
        assert totals["FY2024"] == 944000
        assert tam_som_module["SEBI_VERIFIED_FY2024_INDUSTRY_UNITS"] == 944000

    def test_yoy_growth_rates_are_calculated(self, tam_som_module):
        df = tam_som_module["build_sebi_market_growth_table"]()
        assert pd.isna(df[df["fiscal_year"] == "FY2021"]["yoy_growth_pct"].iloc[0])
        fy22_growth = df[df["fiscal_year"] == "FY2022"]["yoy_growth_pct"].iloc[0]
        assert abs(fy22_growth - 507.3) < 0.5, f"FY22 growth should be ~507.3%, got {fy22_growth}"
        fy24_growth = df[df["fiscal_year"] == "FY2024"]["yoy_growth_pct"].iloc[0]
        assert abs(fy24_growth - 29.7) < 0.5, f"FY24 growth should be ~29.7%, got {fy24_growth}"

    def test_cagr_is_calculated(self, tam_som_module):
        df = tam_som_module["build_sebi_market_growth_table"]()
        cagr = df["cagr_fy2021_fy2024_pct"].iloc[0]
        expected = round(((944000/41000)**(1/3) - 1) * 100, 1)
        assert abs(cagr - expected) < 0.5, f"CAGR should be {expected}%, got {cagr}"

    def test_provenance_is_verified(self, tam_som_module):
        df = tam_som_module["build_sebi_market_growth_table"]()
        assert all(df["provenance_status"] == "verified_primary_source")
        assert "SEBI" in tam_som_module["SEBI_VERIFIED_SOURCE"]


class TestTAMSAMSOM:
    def test_tam_base_anchored_to_sebi_verified_fy2024(self, tam_som_module):
        tam = tam_som_module["compute_tam"]("base")
        assert tam["verified_anchor"]["fy2024_industry_units"] == 944000
        assert "SEBI" in tam["verified_anchor"]["source"]
        assert "OBSERVED" in tam["verified_anchor"]["data_classification"]

    def test_tam_units_are_positive_for_all_scenarios(self, tam_som_module):
        for scenario in ["conservative", "base", "upside"]:
            tam = tam_som_module["compute_tam"](scenario)
            assert tam["tam_units"] > 944000, f"TAM should exceed FY24 baseline for {scenario}"
            assert tam["tam_revenue_inr_crore"] > 0

    def test_sam_is_subset_of_tam(self, tam_som_module):
        for scenario in ["conservative", "base", "upside"]:
            tam = tam_som_module["compute_tam"](scenario)
            sam = tam_som_module["compute_sam"](scenario)
            assert sam["sam_units"] < tam["tam_units"]

    def test_som_is_subset_of_sam(self, tam_som_module):
        for scenario in ["conservative", "base", "upside"]:
            sam = tam_som_module["compute_sam"](scenario)
            som = tam_som_module["compute_som"](scenario)
            assert som["som_units"] < sam["sam_units"]

    def test_assumptions_are_labelled(self, tam_som_module):
        tam = tam_som_module["compute_tam"]("base")
        assert "ASSUMPTION" in tam["assumptions"]["data_classification"]
        assert "ASSUMPTION" in tam["assumptions"]["growth_basis"]

    def test_build_table_has_three_scenarios(self, tam_som_module):
        df = tam_som_module["build_tam_sam_som_table"]()
        assert len(df) == 3
        assert set(df["scenario"]) == {"Conservative Case", "Base Case", "Upside Case"}

    def test_som_lt_sam_lt_tam_for_all_scenarios(self, tam_som_module):
        df = tam_som_module["build_tam_sam_som_table"]()
        for _, row in df.iterrows():
            assert row["som_units"] < row["sam_units"] < row["tam_units"], (
                f"SOM < SAM < TAM violated for {row['scenario']}"
            )

    def test_invalid_scenario_raises(self, tam_som_module):
        with pytest.raises(ValueError):
            tam_som_module["compute_tam"]("fantasy_scenario")


class TestGAIFramework:
    def test_gai_5_factor_weights(self):
        from analytics.geographic_analysis import GAI_WEIGHTS
        assert len(GAI_WEIGHTS) == 5
        assert GAI_WEIGHTS["registration_volume_score"] == 0.30
        assert GAI_WEIGHTS["per_capita_income_score"] == 0.25
        assert GAI_WEIGHTS["two_w_density_score"] == 0.20
        assert GAI_WEIGHTS["ev_policy_score"] == 0.15
        assert GAI_WEIGHTS["urbanization_score"] == 0.10
        assert round(sum(GAI_WEIGHTS.values()), 4) == 1.0

    def test_gai_fail_closed_on_missing_column(self):
        from analytics.geographic_analysis import compute_gai_scores
        df_incomplete = pd.DataFrame({
            "state": ["Maharashtra", "Karnataka"],
            "registration_volume_score": [95.0, 85.0],
            # missing income, density, policy, urbanization
        })
        res = compute_gai_scores(df_incomplete)
        assert "INCOMPLETE" in res["status"].iloc[0]

    def test_gai_fail_closed_on_null_values(self):
        from analytics.geographic_analysis import compute_gai_scores
        df = pd.DataFrame({
            "state": ["State A", "State B"],
            "registration_volume_score": [90.0, None],  # State B has missing registration volume
            "per_capita_income_score": [80.0, 70.0],
            "two_w_density_score": [75.0, 65.0],
            "ev_policy_score": [85.0, 60.0],
            "urbanization_score": [70.0, 50.0],
        })
        res = compute_gai_scores(df)
        state_b = res[res["state"] == "State B"].iloc[0]
        assert pd.isna(state_b["gai_score"])
        assert pd.isna(state_b["gai_rank"])
        assert "INCOMPLETE" in state_b["data_quality_status"]

    def test_gai_complete_data_scores_and_ranks(self):
        from analytics.geographic_analysis import compute_gai_scores
        df = pd.DataFrame({
            "state": ["State A", "State B", "State C"],
            "registration_volume_score": [100.0, 50.0, 10.0],
            "per_capita_income_score": [100.0, 60.0, 20.0],
            "two_w_density_score": [90.0, 70.0, 30.0],
            "ev_policy_score": [80.0, 50.0, 40.0],
            "urbanization_score": [70.0, 60.0, 50.0],
        })
        res = compute_gai_scores(df)
        assert len(res) == 3
        assert (res["data_quality_status"] == "COMPLETE").all()
        # State A has highest in all categories, so its normalized score must be highest
        assert res.loc[res["state"] == "State A", "gai_rank"].iloc[0] == 1
        assert res.loc[res["state"] == "State C", "gai_rank"].iloc[0] == 3


class TestReconciliation:
    def test_sebi_market_growth_reconciliation(self, tam_som_module):
        import duckdb
        import zipfile
        root = Path(__file__).resolve().parents[2]

        # 1. Python calculation
        py_df = tam_som_module["build_sebi_market_growth_table"]()
        py_totals = dict(zip(py_df["fiscal_year"], py_df["industry_e2w_units"]))

        # 2. DuckDB SQL Mart
        db_path = root / "data" / "processed" / "sql" / "e2w_sql.duckdb"
        assert db_path.exists(), "DuckDB database not found"
        conn = duckdb.connect(str(db_path))
        sql_df = conn.execute("SELECT fiscal_year, industry_e2w_units FROM mart.sebi_market_growth").fetch_df()
        conn.close()
        sql_totals = dict(zip(sql_df["fiscal_year"], sql_df["industry_e2w_units"]))

        # 3. Processed CSV
        csv_path = root / "data" / "processed" / "sql" / "sql_sebi_market_growth.csv"
        assert csv_path.exists(), "CSV output not found"
        csv_df = pd.read_csv(csv_path)
        csv_totals = dict(zip(csv_df["fiscal_year"], csv_df["industry_e2w_units"]))

        # 4. Excel Workbook sheet6
        wb_path = root / "outputs" / "Market_Business_Strategy_Intelligence.xlsx"
        assert wb_path.exists(), "Excel workbook not found"
        with zipfile.ZipFile(wb_path, "r") as z:
            sheet6_content = z.read("xl/worksheets/sheet6.xml").decode("utf-8")

        for fy in ["FY2021", "FY2022", "FY2023", "FY2024"]:
            assert py_totals[fy] == sql_totals[fy] == csv_totals[fy], (
                f"Mismatch in {fy}: Python={py_totals[fy]}, SQL={sql_totals[fy]}, CSV={csv_totals[fy]}"
            )
            assert str(py_totals[fy]) in sheet6_content, f"Excel sheet missing {py_totals[fy]} for {fy}"

    def test_tam_sam_som_reconciliation(self, tam_som_module):
        import duckdb
        import zipfile
        root = Path(__file__).resolve().parents[2]

        # 1. Python calculation
        py_df = tam_som_module["build_tam_sam_som_table"]()
        py_base = py_df[py_df["scenario"] == "Base Case"].iloc[0]

        # 2. DuckDB SQL Mart
        db_path = root / "data" / "processed" / "sql" / "e2w_sql.duckdb"
        conn = duckdb.connect(str(db_path))
        sql_df = conn.execute("SELECT * FROM mart.tam_sam_som WHERE scenario = 'Base Case'").fetch_df()
        conn.close()
        sql_base = sql_df.iloc[0]

        # 3. CSV
        csv_path = root / "data" / "processed" / "sql" / "sql_tam_sam_som.csv"
        csv_df = pd.read_csv(csv_path)
        csv_base = csv_df[csv_df["scenario"] == "Base Case"].iloc[0]

        # 4. Excel sheet7
        wb_path = root / "outputs" / "Market_Business_Strategy_Intelligence.xlsx"
        with zipfile.ZipFile(wb_path, "r") as z:
            sheet7_content = z.read("xl/worksheets/sheet7.xml").decode("utf-8")

        # Verify TAM, SAM, SOM units reconcile across all representations
        assert py_base["tam_units"] == sql_base["tam_units"] == csv_base["tam_units"] == 1180000
        assert py_base["sam_units"] == sql_base["sam_units"] == csv_base["sam_units"] == 660800
        assert py_base["som_units"] == sql_base["som_units"] == csv_base["som_units"] == 19824

        assert str(1180000) in sheet7_content
        assert str(660800) in sheet7_content
        assert str(19824) in sheet7_content
