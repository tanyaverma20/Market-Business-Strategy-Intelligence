from __future__ import annotations

import csv
import json
from pathlib import Path

import duckdb
import pandas as pd


def run_sql_pipeline(db_path: str | None = None, project_root: str | None = None):
    project_root = Path(project_root or Path(__file__).resolve().parents[1])
    db_path = Path(db_path or project_root / "data" / "processed" / "sql" / "e2w_sql.duckdb")
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = duckdb.connect(str(db_path))

    sql_dir = project_root / "sql"
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
            raise FileNotFoundError(f"Missing SQL script: {script_path}")
        sql = script_path.read_text(encoding="utf-8")
        conn.execute(sql)

    verified_rows = conn.execute("SELECT COUNT(*) FROM stg_verified_products").fetchone()[0]
    manufacturer_count = conn.execute("SELECT COUNT(DISTINCT manufacturer) FROM stg_verified_products").fetchone()[0]
    product_count = conn.execute("SELECT COUNT(DISTINCT model_name) FROM stg_verified_products").fetchone()[0]

    quality_issues = conn.execute("SELECT SUM(issue_count) FROM sql_data_quality_results").fetchone()[0]
    pending_market_status = conn.execute("SELECT status FROM pending.market_queries_template LIMIT 1").fetchone()[0]
    pending_market_rows = conn.execute("SELECT COUNT(*) FROM pending.fact_ev_registrations").fetchone()[0]

    outputs_dir = project_root / "data" / "processed" / "sql"
    outputs_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "competitive_analysis_csv": outputs_dir / "sql_competitive_analysis.csv",
        "pricing_analysis_csv": outputs_dir / "sql_pricing_analysis.csv",
        "product_positioning_csv": outputs_dir / "sql_product_positioning.csv",
        "kpi_results_csv": outputs_dir / "sql_kpi_results.csv",
        "data_quality_csv": outputs_dir / "sql_data_quality_results.csv",
    }

    for name, path in outputs.items():
        if name == "competitive_analysis_csv":
            df = conn.execute("SELECT * FROM mart_competitive_analysis ORDER BY manufacturer, product_rank").fetch_df()
        elif name == "pricing_analysis_csv":
            df = conn.execute("SELECT * FROM mart_pricing_analysis ORDER BY manufacturer, product").fetch_df()
        elif name == "product_positioning_csv":
            df = conn.execute("SELECT * FROM mart_product_positioning ORDER BY manufacturer, model_name").fetch_df()
        elif name == "kpi_results_csv":
            df = conn.execute("SELECT * FROM kpi_status ORDER BY kpi_name").fetch_df()
        elif name == "data_quality_csv":
            df = conn.execute("SELECT * FROM sql_data_quality_results ORDER BY check_name").fetch_df()
        df.to_csv(path, index=False)

    result = {
        "db_path": str(db_path),
        "verified_product_rows": int(verified_rows),
        "manufacturer_count": int(manufacturer_count),
        "product_count": int(product_count),
        "quality_issues": int(quality_issues or 0),
        "pending_market_rows": int(pending_market_rows),
        "pending_market_status": str(pending_market_status),
        "outputs": outputs,
    }

    with (outputs_dir / "sql_pipeline_summary.json").open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, default=str)

    conn.close()
    return result


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
