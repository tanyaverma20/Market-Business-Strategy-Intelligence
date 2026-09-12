from pathlib import Path
import duckdb
import pytest

from run_sql_pipeline import run_sql_pipeline


@pytest.fixture(scope="module")
def sql_pipeline_result(tmp_path_factory):
    project_root = Path(__file__).resolve().parents[2]
    tmp_dir = tmp_path_factory.mktemp("sql_test")
    db_path = tmp_dir / "e2w_sql_test.duckdb"
    return run_sql_pipeline(db_path=str(db_path), project_root=str(project_root)), db_path


def test_sql_pipeline_creates_verified_warehouse(sql_pipeline_result):
    result, _ = sql_pipeline_result

    assert result["verified_product_rows"] >= 25
    assert result["verified_product_rows"] == 42
    assert result["manufacturer_count"] >= 10
    assert result["manufacturer_count"] == 11
    assert result["product_count"] >= 25
    assert result["product_count"] == 42
    assert result["quality_issues"] == 0

    # Verify all 5 output CSV files exist and are populated
    for key, path in result["outputs"].items():
        p = Path(path)
        assert p.exists(), f"Missing output CSV: {p}"
        assert p.stat().st_size > 0, f"Empty output CSV: {p}"


def test_sql_pipeline_keeps_market_data_pending(sql_pipeline_result):
    result, _ = sql_pipeline_result

    assert result["pending_market_rows"] == 0
    assert result["pending_market_status"] == "PENDING VERIFIED VAHAN DATA"


def test_sql_tables_and_views_structure(sql_pipeline_result):
    _, db_path = sql_pipeline_result
    conn = duckdb.connect(str(db_path))

    # Verify key staging, dimensions, and facts exist
    tables = [r[0] for r in conn.execute("SHOW TABLES").fetchall()]
    expected_tables = [
        "stg_verified_products",
        "dim_manufacturer",
        "dim_product",
        "fact_product_metrics",
        "sql_data_quality_results",
    ]
    for table in expected_tables:
        assert table in tables, f"Expected table '{table}' not found in database"

    # Verify key marts and KPI views exist
    expected_views = [
        "mart_competitive_analysis",
        "mart_pricing_analysis",
        "mart_product_positioning",
        "kpi_status",
    ]
    for view in expected_views:
        assert view in tables, f"Expected view '{view}' not found in database"

    conn.close()


def test_sql_data_quality_integrity(sql_pipeline_result):
    _, db_path = sql_pipeline_result
    conn = duckdb.connect(str(db_path))

    dq_checks = conn.execute("SELECT check_name, issue_count FROM sql_data_quality_results").fetchall()
    assert len(dq_checks) == 10, f"Expected 10 DQ checks, found {len(dq_checks)}"

    for check_name, issue_count in dq_checks:
        assert issue_count == 0, f"Data quality failure in '{check_name}': {issue_count} issues found"

    conn.close()


def test_sql_window_functions_and_rankings(sql_pipeline_result):
    _, db_path = sql_pipeline_result
    conn = duckdb.connect(str(db_path))

    # 1. Competitive analysis rankings
    comp_df = conn.execute(
        "SELECT manufacturer, product, price, manufacturer_rank, product_rank, price_efficiency_rank "
        "FROM mart_competitive_analysis"
    ).fetch_df()
    assert not comp_df.empty
    assert (comp_df["manufacturer_rank"] >= 1).all()
    assert (comp_df["product_rank"] >= 1).all()

    # 2. Pricing mart percentiles and quartiles
    price_df = conn.execute(
        "SELECT product, price, price_percentile, price_quartile, relative_price_position "
        "FROM mart_pricing_analysis WHERE price IS NOT NULL"
    ).fetch_df()
    assert not price_df.empty
    assert (price_df["price_percentile"] >= 0.0).all() and (price_df["price_percentile"] <= 1.0).all()
    assert price_df["price_quartile"].isin([1, 2, 3, 4]).all()
    assert set(price_df["relative_price_position"].unique()).issubset({
        "below market average", "above market average", "at market average"
    })

    conn.close()


def test_sql_product_positioning_buckets(sql_pipeline_result):
    _, db_path = sql_pipeline_result
    conn = duckdb.connect(str(db_path))

    pos_df = conn.execute(
        "SELECT manufacturer, model_name, price_bucket, range_bucket, battery_bucket, performance_bucket "
        "FROM mart_product_positioning"
    ).fetch_df()
    assert len(pos_df) >= 25
    assert len(pos_df) == 42

    valid_price_buckets = {"budget", "mid-market", "premium", "unpriced"}
    valid_range_buckets = {"short-range", "standard-range", "long-range", "unspecified"}
    valid_battery_buckets = {"compact-battery", "standard-battery", "high-battery", "unspecified"}
    valid_perf_buckets = {"entry", "balanced", "high-performance", "unspecified"}

    assert set(pos_df["price_bucket"].unique()).issubset(valid_price_buckets)
    assert set(pos_df["range_bucket"].unique()).issubset(valid_range_buckets)
    assert set(pos_df["battery_bucket"].unique()).issubset(valid_battery_buckets)
    assert set(pos_df["performance_bucket"].unique()).issubset(valid_perf_buckets)

    conn.close()


def test_no_proxy_market_data_in_factual_sql_outputs(sql_pipeline_result):
    _, db_path = sql_pipeline_result
    conn = duckdb.connect(str(db_path))

    # Verify pending schema table has 0 rows
    pending_count = conn.execute("SELECT COUNT(*) FROM pending.fact_ev_registrations").fetchone()[0]
    assert pending_count == 0

    # Verify templates explicitly state status
    templates = conn.execute("SELECT query_name, status FROM pending.market_queries_template").fetchall()
    assert len(templates) == 8
    for qname, status in templates:
        assert status == "PENDING VERIFIED VAHAN DATA"

    # Verify all products in dimension and fact tables are from verified source
    dim_status = conn.execute("SELECT DISTINCT verification_status FROM dim_product").fetchall()
    assert dim_status == [("verified",)]

    conn.close()
