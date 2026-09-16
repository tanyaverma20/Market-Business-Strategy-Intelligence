"""
Power BI PBIP Path Patcher
==========================
This script patches the DATA_PATH placeholder in the model.bim file
with the actual absolute path to the SQL data mart CSVs.

Run this script ONCE after cloning or moving the repository:
    python powerbi/patch_pbip_paths.py

The PBIP project is then ready to open in Power BI Desktop.
"""

import json
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(REPO_ROOT, "data", "processed", "sql")
MODEL_BIM = os.path.join(REPO_ROOT, "powerbi",
                         "Market-Business-Strategy-Intelligence.SemanticModel",
                         "definition", "model.bim")

def patch_model(data_path: str, model_path: str) -> None:
    if not os.path.exists(model_path):
        print(f"ERROR: model.bim not found at {model_path}")
        sys.exit(1)

    with open(model_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Validate required CSVs exist
    required_files = [
        "sql_competitive_analysis.csv",
        "sql_pricing_analysis.csv",
        "sql_product_positioning.csv",
        "sql_kpi_results.csv",
    ]
    missing = [f for f in required_files if not os.path.exists(os.path.join(data_path, f))]
    if missing:
        print(f"WARNING: Missing data files: {missing}")
        print("Run 'python src/run_sql_pipeline.py' first to regenerate data marts.")

    # Replace placeholder — use double backslash for JSON string embedding
    normalized = data_path.replace("/", "\\")
    patched = content.replace("DATA_PATH", normalized)

    with open(model_path, "w", encoding="utf-8") as f:
        f.write(patched)

    print(f"[OK] model.bim patched successfully.")
    print(f"  Data path: {normalized}")
    print(f"  Files found: {[f for f in required_files if os.path.exists(os.path.join(data_path, f))]}")

    # Also sync non-definition model.bim if it exists
    alt_model = os.path.join(REPO_ROOT, "powerbi",
                             "Market-Business-Strategy-Intelligence.SemanticModel",
                             "model.bim")
    if os.path.exists(alt_model):
        with open(alt_model, "w", encoding="utf-8") as f:
            f.write(patched)

    print()
    print("NEXT STEPS:")
    print("1. Open Power BI Desktop")
    print(f"2. File -> Open -> {os.path.join(REPO_ROOT, 'powerbi', 'Market-Business-Strategy-Intelligence.pbip')}")
    print("3. Allow data source connection (local files, no credentials needed)")
    print("4. Click 'Refresh' to load all tables")
    print("5. Verify all 5 pages render correctly")
    print("6. File -> Save As -> Market-Business-Strategy-Intelligence.pbix")
    print(f"7. Save to: {REPO_ROOT}")
    print()
    print("SCREENSHOT EXPORT (after saving .pbix):")
    print("  In Power BI Desktop: File -> Export -> Export to PDF, or")
    print("  For each page: right-click page tab -> 'Export page as image'")
    print(f"  Save screenshots to: {os.path.join(REPO_ROOT, 'docs', 'powerbi', 'screenshots')}")
    print("  Filenames: page1_executive_overview.png through page5_strategy.png")

if __name__ == "__main__":
    patch_model(DATA_PATH, MODEL_BIM)
