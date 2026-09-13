from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile
import pandas as pd
import pytest


@pytest.fixture(scope="module")
def project_root():
    return Path(__file__).resolve().parents[2]


def test_verified_manufacturer_count_meets_resume_claim(project_root):
    catalog_path = project_root / "data" / "processed" / "processed_verified_product_catalog.csv"
    assert catalog_path.exists()

    df = pd.read_csv(catalog_path)
    verified_mfgs = df[df["verification_status"] == "verified"]["manufacturer"].unique()

    # Resume Claim 2 requires "10+ competitors"
    assert len(verified_mfgs) >= 10, f"Expected >= 10 verified manufacturers, found {len(verified_mfgs)}"
    assert len(verified_mfgs) == 11


def test_verified_product_count_meets_resume_claim(project_root):
    catalog_path = project_root / "data" / "processed" / "processed_verified_product_catalog.csv"
    df = pd.read_csv(catalog_path)
    verified_prods = df[df["verification_status"] == "verified"]["model_name"].unique()

    # Resume Claim 2 requires "25+ products"
    assert len(verified_prods) >= 25, f"Expected >= 25 verified products, found {len(verified_prods)}"
    assert len(verified_prods) == 42


def test_excel_workbook_exists_and_has_seven_sheets(project_root):
    wb_path = project_root / "outputs" / "Market_Business_Strategy_Intelligence.xlsx"
    assert wb_path.exists(), "Missing Excel analytical workbook"
    assert wb_path.stat().st_size > 5000, "Excel workbook appears empty or corrupted"

    # Inspect sheets via OpenXML container
    with zipfile.ZipFile(wb_path, "r") as z:
        tree = ET.fromstring(z.read("xl/workbook.xml"))
        sheet_names = [elem.attrib["name"] for elem in tree.iter("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}sheet")]

    expected_sheets = [
        "Executive_KPI_Summary",
        "Competitive_Benchmark",
        "Pricing_Analysis",
        "Product_Positioning",
        "Strategic_Recommendations",
        "Source_Register",
        "Assumptions_Provenance"
    ]
    for expected in expected_sheets:
        assert expected in sheet_names, f"Expected sheet '{expected}' missing from Excel workbook"


def test_final_kpi_registry_contains_at_least_15_verified_kpis(project_root):
    kpi_doc_path = project_root / "docs" / "FINAL_KPI_REGISTRY.md"
    assert kpi_doc_path.exists()

    content = kpi_doc_path.read_text(encoding="utf-8")
    assert "24 Verified KPIs" in content or "VERIFIED" in content

    # Count rows in verified table
    verified_rows = [line for line in content.splitlines() if "**VERIFIED**" in line or "| **" in line and "VERIFIED" in line]
    assert len(verified_rows) >= 15, f"Expected >= 15 verified KPIs in registry, found {len(verified_rows)}"


def test_no_proxy_data_relabeled_as_verified(project_root):
    manifest_path = project_root / "data" / "raw" / "DATASET_MANIFEST.csv"
    manifest_df = pd.read_csv(manifest_path)

    # Ensure proxy datasets are never marked as eligible for observed analytics
    proxy_rows = manifest_df[manifest_df["provenance_class"] == "generated_proxy"]
    assert not proxy_rows.empty
    assert (proxy_rows["eligible_as_observed_analytics"] == "No").all(), "Found proxy data marked as eligible for observed analytics"


def test_product_portfolio_hhi_regression(project_root):
    """Regression test: Product Portfolio HHI must equal 1,326.53 (±0.5 tolerance).

    Calculation (verified 2026-09-13):
      - 42 verified models across 11 manufacturers in verified_product_catalog_2025_2026.csv
      - Each manufacturer share = (model_count / 42) * 100
      - HHI = SUM(share^2) across all 11 manufacturers
    Expected: 1326.53

    The previously documented value of 2,333.3 was INCORRECT.
    Do NOT adjust this constant to match a broken result — investigate root cause.
    """
    catalog_path = project_root / "data" / "processed" / "processed_verified_product_catalog.csv"
    assert catalog_path.exists(), "Verified product catalog not found"

    df = pd.read_csv(catalog_path)
    verified_df = df[df["verification_status"] == "verified"]

    total_products = len(verified_df)
    assert total_products == 42, f"Expected 42 verified products, got {total_products}"

    mfg_counts = verified_df.groupby("manufacturer").size()
    shares = (mfg_counts / total_products * 100)
    hhi = float((shares ** 2).sum())

    # HHI must be 1326.53 ± 0.5 tolerance for floating-point safety
    assert abs(hhi - 1326.53) < 0.5, (
        f"Product Portfolio HHI regression: computed {hhi:.2f}, expected ~1326.53. "
        f"Check manufacturer grouping, product count, or HHI formula."
    )
