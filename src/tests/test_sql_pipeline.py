from pathlib import Path

from run_sql_pipeline import run_sql_pipeline


def test_sql_pipeline_creates_verified_warehouse(tmp_path):
    project_root = Path(__file__).resolve().parents[2]
    db_path = tmp_path / "e2w_sql.duckdb"

    result = run_sql_pipeline(db_path=str(db_path), project_root=str(project_root))

    assert result["verified_product_rows"] > 0
    assert result["manufacturer_count"] > 0
    assert result["product_count"] > 0
    assert result["quality_issues"] >= 0
    assert result["outputs"]["competitive_analysis_csv"].exists()
    assert result["outputs"]["pricing_analysis_csv"].exists()
    assert result["outputs"]["product_positioning_csv"].exists()
    assert result["outputs"]["kpi_results_csv"].exists()
    assert result["outputs"]["data_quality_csv"].exists()


def test_sql_pipeline_keeps_market_data_pending(tmp_path):
    project_root = Path(__file__).resolve().parents[2]
    db_path = tmp_path / "e2w_sql_pending.duckdb"

    result = run_sql_pipeline(db_path=str(db_path), project_root=str(project_root))

    assert result["pending_market_rows"] == 0
    assert result["pending_market_status"] == "PENDING VERIFIED VAHAN DATA"
