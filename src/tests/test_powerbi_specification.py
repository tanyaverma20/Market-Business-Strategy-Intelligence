from pathlib import Path
import re
import pandas as pd
import pytest


@pytest.fixture(scope="module")
def project_root():
    return Path(__file__).resolve().parents[2]


def test_powerbi_doc_files_exist(project_root):
    expected_docs = [
        "docs/POWER_BI_MODEL.md",
        "docs/POWER_BI_DAX.md",
        "docs/POWER_BI_POWER_QUERY.md",
        "docs/POWER_BI_KPI_MAPPING.md",
        "docs/POWER_BI_DASHBOARD_SPEC.md",
    ]
    for doc in expected_docs:
        doc_path = project_root / doc
        assert doc_path.exists(), f"Missing required documentation: {doc}"
        assert doc_path.stat().st_size > 500, f"Documentation file too short: {doc}"


def test_powerbi_script_files_exist(project_root):
    m_script = project_root / "powerbi" / "power_query_m_scripts.m"
    dax_script = project_root / "powerbi" / "dax_measures.dax"

    assert m_script.exists(), "Missing powerbi/power_query_m_scripts.m"
    assert dax_script.exists(), "Missing powerbi/dax_measures.dax"
    assert m_script.stat().st_size > 1000
    assert dax_script.stat().st_size > 1000


def test_dax_measures_syntactic_integrity(project_root):
    dax_content = (project_root / "powerbi" / "dax_measures.dax").read_text(encoding="utf-8")

    # Verify key DAX keywords and functions
    required_keywords = [
        "CALCULATE",
        "DIVIDE",
        "DISTINCTCOUNT",
        "AVERAGE",
        "MEDIAN",
        "MIN",
        "MAX",
        "COUNTROWS",
        "FILTER",
        "ALL",
    ]
    for kw in required_keywords:
        assert kw in dax_content, f"Expected DAX function/keyword '{kw}' missing from measure library"

    # Count distinct measures defined with '='
    measure_lines = [
        line.strip() for line in dax_content.splitlines() 
        if line.strip() and not line.strip().startswith("//") and not line.strip().startswith("/*") and "=" in line
    ]
    assert len(measure_lines) >= 20, f"Expected at least 20 DAX measures, found {len(measure_lines)}"

    # Check parentheses balance
    open_parens = dax_content.count("(")
    close_parens = dax_content.count(")")
    assert open_parens == close_parens, f"Unbalanced parentheses in DAX file: {open_parens} open vs {close_parens} close"


def test_dax_column_references_align_with_sql_marts(project_root):
    # Verify that the underlying CSV files exist and contain the columns referenced by the DAX library
    sql_dir = project_root / "data" / "processed" / "sql"
    comp_csv = sql_dir / "sql_competitive_analysis.csv"
    pricing_csv = sql_dir / "sql_pricing_analysis.csv"
    pos_csv = sql_dir / "sql_product_positioning.csv"

    assert comp_csv.exists()
    assert pricing_csv.exists()
    assert pos_csv.exists()

    comp_df = pd.read_csv(comp_csv)
    pricing_df = pd.read_csv(pricing_csv)
    pos_df = pd.read_csv(pos_csv)

    # Core columns referenced in DAX
    assert "product" in comp_df.columns
    assert "price" in comp_df.columns
    assert "battery_kwh" in comp_df.columns
    assert "certified_range_km" in comp_df.columns
    assert "top_speed_kmph" in comp_df.columns
    assert "price_per_km" in comp_df.columns
    assert "price_per_kwh" in comp_df.columns

    assert "relative_price_position" in pricing_df.columns
    assert "price_bucket" in pos_df.columns
    assert "range_bucket" in pos_df.columns
    assert "performance_bucket" in pos_df.columns


def test_pending_market_measures_return_blank(project_root):
    dax_content = (project_root / "powerbi" / "dax_measures.dax").read_text(encoding="utf-8")

    pending_measures = [
        "Total EV Registrations (Pending)",
        "YoY Market Growth Pct (Pending)",
        "Market CAGR Pct (Pending)",
        "EV Penetration Pct (Pending)",
        "OEM Registration Market Share Pct (Pending)",
        "Market Volume HHI (Pending)",
        "State Registration Rank (Pending)",
    ]

    for measure in pending_measures:
        assert measure in dax_content, f"Missing pending market measure: {measure}"
        # Ensure it returns BLANK()
        pattern = rf"{re.escape(measure)}\s*=\s*BLANK\(\)"
        assert re.search(pattern, dax_content), f"Pending measure {measure} must return BLANK()"


def test_dashboard_spec_covers_five_pages(project_root):
    spec_content = (project_root / "docs" / "POWER_BI_DASHBOARD_SPEC.md").read_text(encoding="utf-8")

    required_pages = [
        "Page 1 — Executive Market & Business Overview",
        "Page 2 — Product & Competitive Intelligence",
        "Page 3 — Pricing & Value Analysis",
        "Page 4 — Product Positioning",
        "Page 5 — Strategy & Opportunity Framework",
    ]

    for page in required_pages:
        assert page in spec_content, f"Dashboard specification missing section for {page}"


# ── PBIP Project Structure Tests ─────────────────────────────────────────────

def test_pbip_project_entry_file_valid(project_root):
    """The .pbip entry file must be valid JSON with version + artifacts keys."""
    import json
    pbip = project_root / "powerbi" / "Market-Business-Strategy-Intelligence.pbip"
    assert pbip.exists(), "Missing Market-Business-Strategy-Intelligence.pbip"
    with open(pbip, encoding="utf-8") as f:
        d = json.load(f)
    assert "version" in d, "PBIP entry file missing 'version'"
    assert "artifacts" in d, "PBIP entry file missing 'artifacts'"


def test_pbip_report_json_five_pages(project_root):
    """report.json must be valid JSON with exactly 5 named report pages."""
    import json
    rjson = (
        project_root / "powerbi"
        / "Market-Business-Strategy-Intelligence.Report"
        / "definition" / "report.json"
    )
    assert rjson.exists(), "Missing Report/definition/report.json"
    with open(rjson, encoding="utf-8") as f:
        d = json.load(f)
    pages = d.get("sections", [])
    assert len(pages) == 5, f"Expected 5 report pages, got {len(pages)}"
    page_names = [p.get("displayName", "") for p in pages]
    assert any("Executive" in n for n in page_names), "Missing Executive page"
    assert any("Competitive" in n for n in page_names), "Missing Competitive page"
    assert any("Pricing" in n for n in page_names), "Missing Pricing page"
    assert any("Positioning" in n for n in page_names), "Missing Positioning page"
    assert any("Strategy" in n for n in page_names), "Missing Strategy page"
    total_vc = sum(len(p.get("visualContainers", [])) for p in pages)
    assert total_vc >= 30, f"Expected 30+ visual containers, got {total_vc}"


def test_pbip_model_bim_valid_and_fail_closed(project_root):
    """model.bim must be valid JSON; pending measures must return BLANK()."""
    import json
    mbim = (
        project_root / "powerbi"
        / "Market-Business-Strategy-Intelligence.SemanticModel"
        / "definition" / "model.bim"
    )
    assert mbim.exists(), "Missing SemanticModel/definition/model.bim"
    with open(mbim, encoding="utf-8") as f:
        d = json.load(f)
    tables = d["model"]["tables"]
    table_names = [t["name"] for t in tables]
    assert "CompetitiveAnalysis" in table_names
    assert "PricingAnalysis" in table_names
    assert "ProductPositioning" in table_names
    assert "KPIStatus" in table_names
    assert "_Measures" in table_names

    measures_table = next(t for t in tables if t["name"] == "_Measures")
    measures = measures_table["measures"]
    assert len(measures) >= 30, f"Expected 30+ DAX measures, got {len(measures)}"

    pending = [m for m in measures if "PENDING" in m["name"]]
    assert len(pending) >= 5, f"Expected 5+ pending measures, got {len(pending)}"
    for m in pending:
        assert m["expression"] == "BLANK()", (
            f"Pending measure '{m['name']}' must return BLANK(), got: {m['expression']}"
        )
