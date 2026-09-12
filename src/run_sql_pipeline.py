from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict

import duckdb
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("sql_pipeline")


def run_sql_pipeline(db_path: str | None = None, project_root: str | None = None) -> Dict[str, Any]:
    """
    Executes the DuckDB SQL analytical pipeline:
    1. Connects to/initializes the local DuckDB database.
    2. Runs schema initialization, data loading with provenance, data quality validation,
       competitive analysis, pricing analysis, product positioning, KPI views,
       and pending market templates.
    3. Verifies data quality results and enforces fail-closed safeguards.
    4. Generates standardized CSV and JSON analytics outputs.
    """
    project_root_path = Path(project_root or Path(__file__).resolve().parents[1]).resolve()
    db_file = Path(db_path or project_root_path / "data" / "processed" / "sql" / "e2w_sql.duckdb").resolve()
    db_file.parent.mkdir(parents=True, exist_ok=True)

    csv_catalog_path = (project_root_path / "data" / "processed" / "processed_verified_product_catalog.csv").resolve().as_posix()
    if not Path(csv_catalog_path).exists():
        # Fallback to raw catalog if processed is missing
        csv_catalog_path = (project_root_path / "data" / "raw" / "verified_product_catalog_2025_2026.csv").resolve().as_posix()

    logger.info(f"Connecting to DuckDB at: {db_file}")
    conn = duckdb.connect(str(db_file))

    sql_dir = project_root_path / "sql"
    scripts = [
        "01_schema.sql",
        "02_load_verified_data.sql",
        "03_data_quality.sql",
        "04_competitive_analysis.sql",
        "05_pricing_analysis.sql",
        "06_product_positioning.sql",
        "07_kpi_queries.sql",
        "08_pending_market_queries.sql",
    ]

    for script_name in scripts:
        script_path = sql_dir / script_name
        if not script_path.exists():
            raise FileNotFoundError(f"Missing required SQL script: {script_path}")
        
        logger.info(f"Executing SQL script: {script_name}")
        sql = script_path.read_text(encoding="utf-8")

        # Dynamically inject the exact absolute path to the verified catalog CSV in script 02
        if script_name == "02_load_verified_data.sql":
            sql = sql.replace("'data/processed/processed_verified_product_catalog.csv'", f"'{csv_catalog_path}'")

        conn.execute(sql)

    # 1. Query verified catalog counts
    verified_rows = conn.execute("SELECT COUNT(*) FROM stg_verified_products").fetchone()[0]
    mfg_count = conn.execute("SELECT COUNT(DISTINCT manufacturer) FROM stg_verified_products").fetchone()[0]
    prod_count = conn.execute("SELECT COUNT(DISTINCT model_name) FROM stg_verified_products").fetchone()[0]

    # 2. Check Data Quality validations
    dq_df = conn.execute("SELECT check_name, issue_count, description FROM sql_data_quality_results").fetch_df()
    total_dq_issues = int(dq_df["issue_count"].sum())
    failed_checks = dq_df[dq_df["issue_count"] > 0]

    if total_dq_issues > 0:
        issues_summary = failed_checks.to_dict(orient="records")
        logger.error(f"CRITICAL: SQL Data Quality issues detected: {issues_summary}")
        raise ValueError(f"SQL pipeline aborted due to {total_dq_issues} data quality failure(s): {issues_summary}")
    else:
        logger.info("SQL Data Quality: All 10 checks passed with 0 issues.")

    # 3. Fail-Closed Safeguard: Verify pending market data is strictly empty
    pending_market_rows = conn.execute("SELECT COUNT(*) FROM pending.fact_ev_registrations").fetchone()[0]
    if pending_market_rows > 0:
        raise ValueError("CRITICAL PROVENANCE VIOLATION: pending.fact_ev_registrations contains unverified data!")

    pending_templates_count = conn.execute("SELECT COUNT(*) FROM pending.market_queries_template").fetchone()[0]
    pending_status = conn.execute("SELECT status FROM pending.market_queries_template LIMIT 1").fetchone()[0]

    # 4. Generate CSV Outputs
    outputs_dir = project_root_path / "data" / "processed" / "sql"
    outputs_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "competitive_analysis_csv": outputs_dir / "sql_competitive_analysis.csv",
        "pricing_analysis_csv": outputs_dir / "sql_pricing_analysis.csv",
        "product_positioning_csv": outputs_dir / "sql_product_positioning.csv",
        "kpi_results_csv": outputs_dir / "sql_kpi_results.csv",
        "data_quality_csv": outputs_dir / "sql_data_quality_results.csv",
    }

    # Export marts to CSV
    conn.execute("SELECT * FROM mart_competitive_analysis ORDER BY manufacturer, product").fetch_df().to_csv(
        outputs["competitive_analysis_csv"], index=False
    )
    conn.execute("SELECT * FROM mart_pricing_analysis ORDER BY manufacturer, product").fetch_df().to_csv(
        outputs["pricing_analysis_csv"], index=False
    )
    conn.execute("SELECT * FROM mart_product_positioning ORDER BY manufacturer, model_name").fetch_df().to_csv(
        outputs["product_positioning_csv"], index=False
    )
    conn.execute("SELECT * FROM kpi_status ORDER BY kpi_name").fetch_df().to_csv(
        outputs["kpi_results_csv"], index=False
    )
    dq_df.to_csv(outputs["data_quality_csv"], index=False)

    summary = {
        "db_path": str(db_file),
        "verified_product_rows": int(verified_rows),
        "manufacturer_count": int(mfg_count),
        "product_count": int(prod_count),
        "quality_issues": total_dq_issues,
        "data_quality_checks_run": len(dq_df),
        "pending_market_rows": int(pending_market_rows),
        "pending_market_templates_count": int(pending_templates_count),
        "pending_market_status": str(pending_status),
        "outputs": {k: str(v) for k, v in outputs.items()},
    }

    summary_file = outputs_dir / "sql_pipeline_summary.json"
    with summary_file.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    logger.info(f"SQL Pipeline execution completed successfully. Summary saved to {summary_file}")
    conn.close()

    # Return result with Path objects in outputs dictionary for test compatibility
    return {
        "db_path": str(db_file),
        "verified_product_rows": int(verified_rows),
        "manufacturer_count": int(mfg_count),
        "product_count": int(prod_count),
        "quality_issues": total_dq_issues,
        "pending_market_rows": int(pending_market_rows),
        "pending_market_status": str(pending_status),
        "outputs": outputs,
    }


if __name__ == "__main__":
    result = run_sql_pipeline()
    print(json.dumps({
        "db_path": result["db_path"],
        "verified_product_rows": result["verified_product_rows"],
        "manufacturer_count": result["manufacturer_count"],
        "product_count": result["product_count"],
        "quality_issues": result["quality_issues"],
        "pending_market_status": result["pending_market_status"],
        "output_files": [str(p) for p in result["outputs"].values()],
    }, indent=2))
