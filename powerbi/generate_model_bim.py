"""
Generate a correctly JSON-encoded model.bim with absolute data paths.
Run: python powerbi/generate_model_bim.py
"""
import json
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(REPO_ROOT, "data", "processed", "sql")
OUTPUT = os.path.join(REPO_ROOT, "powerbi",
                      "Market-Business-Strategy-Intelligence.SemanticModel",
                      "definition", "model.bim")


def csv_path(filename):
    return os.path.join(DATA_PATH, filename)


def make_csv_partition(name, csv_file, columns_spec, col_count):
    """Build a partition dict for a CSV-sourced table."""
    col_type_pairs = ", ".join(
        '{"%s", %s}' % (c, t) for c, t in columns_spec
    )
    return {
        "name": name,
        "mode": "import",
        "source": {
            "type": "m",
            "expression": [
                "let",
                (
                    '    Source = Csv.Document(File.Contents("'
                    + csv_path(csv_file).replace("\\", "\\\\")
                    + '"),['
                    + f'Delimiter=",", Columns={col_count}, '
                    + "Encoding=65001, QuoteStyle=QuoteStyle.None]),"
                ),
                "    #\"Promoted Headers\" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),",
                "    #\"Changed Types\" = Table.TransformColumnTypes(#\"Promoted Headers\",{"
                + col_type_pairs
                + "})",
                "in",
                "    #\"Changed Types\"",
            ],
        },
    }


def build_model():
    comp_cols = [
        ("manufacturer", "type text"), ("product", "type text"),
        ("category", "type text"), ("price", "type number"),
        ("battery_kwh", "type number"), ("certified_range_km", "type number"),
        ("top_speed_kmph", "type number"), ("motor_power_kw", "type number"),
        ("price_per_km", "type number"), ("price_per_kwh", "type number"),
        ("manufacturer_rank", "Int64.Type"), ("product_rank", "Int64.Type"),
        ("price_efficiency_rank", "Int64.Type"), ("range_rank", "Int64.Type"),
        ("speed_rank", "Int64.Type"), ("mfg_product_count", "Int64.Type"),
        ("mfg_portfolio_share_pct", "type number"), ("verification_status", "type text"),
    ]

    pricing_cols = [
        ("product", "type text"), ("manufacturer", "type text"),
        ("price", "type number"), ("battery_capacity_kwh", "type number"),
        ("range_km", "type number"), ("top_speed_kmh", "type number"),
        ("price_per_km", "type number"), ("price_per_kwh", "type number"),
        ("price_bucket", "type text"), ("value_rank", "Int64.Type"),
        ("price_percentile", "type number"), ("price_quartile", "Int64.Type"),
        ("product_price_rank", "Int64.Type"), ("avg_market_price", "type number"),
        ("mfg_avg_price", "type number"), ("relative_price_position", "type text"),
        ("price_premium_vs_market_pct", "type number"),
    ]

    pos_cols = [
        ("manufacturer", "type text"), ("model_name", "type text"),
        ("price", "type number"), ("range_km", "type number"),
        ("battery_capacity_kwh", "type number"), ("top_speed_kmh", "type number"),
        ("price_bucket", "type text"), ("range_bucket", "type text"),
        ("battery_bucket", "type text"), ("performance_bucket", "type text"),
        ("positioning_summary", "type text"), ("manufacturer_product_rank", "Int64.Type"),
        ("manufacturer_total_products", "Int64.Type"),
        ("manufacturer_budget_count", "Int64.Type"),
        ("manufacturer_midmarket_count", "Int64.Type"),
        ("manufacturer_premium_count", "Int64.Type"),
        ("manufacturer_portfolio_share_pct", "type number"),
        ("verification_status", "type text"),
    ]

    kpi_cols = [
        ("kpi_name", "type text"), ("value", "type number"),
        ("unit", "type text"), ("source", "type text"),
        ("verification_status", "type text"), ("calculation_date", "type text"),
        ("methodology", "type text"),
    ]

    def col(name, dtype):
        return {"name": name, "dataType": dtype, "sourceColumn": name}

    type_map = {
        "type text": "string", "type number": "double",
        "Int64.Type": "int64",
    }

    def cols_from_spec(spec):
        return [col(n, type_map[t]) for n, t in spec]

    measures = [
        ("Total Products", 'DISTINCTCOUNT(CompetitiveAnalysis[product])', "#,##0"),
        ("Total Manufacturers", 'DISTINCTCOUNT(CompetitiveAnalysis[manufacturer])', "#,##0"),
        ("Priced Products Count",
         'COUNTROWS(FILTER(PricingAnalysis, NOT ISBLANK(PricingAnalysis[price])))', "#,##0"),
        ("Average Product Price",
         'AVERAGEX(FILTER(PricingAnalysis, NOT ISBLANK(PricingAnalysis[price])), PricingAnalysis[price])',
         "#,##0"),
        ("Median Product Price",
         'MEDIANX(FILTER(PricingAnalysis, NOT ISBLANK(PricingAnalysis[price])), PricingAnalysis[price])',
         "#,##0"),
        ("Minimum Product Price",
         'MINX(FILTER(PricingAnalysis, NOT ISBLANK(PricingAnalysis[price])), PricingAnalysis[price])',
         "#,##0"),
        ("Maximum Product Price",
         'MAXX(FILTER(PricingAnalysis, NOT ISBLANK(PricingAnalysis[price])), PricingAnalysis[price])',
         "#,##0"),
        ("Price Spread", "[Maximum Product Price] - [Minimum Product Price]", "#,##0"),
        ("Market Benchmark Average Price",
         'CALCULATE(AVERAGEX(FILTER(PricingAnalysis, NOT ISBLANK(PricingAnalysis[price])), PricingAnalysis[price]), ALL(PricingAnalysis))',
         "#,##0"),
        ("Price Variance vs Market Average",
         "[Average Product Price] - [Market Benchmark Average Price]", "#,##0"),
        ("Price Premium %",
         "DIVIDE([Price Variance vs Market Average], [Market Benchmark Average Price], BLANK()) * 100",
         "#,##0.0"),
        ("Average Battery Capacity",
         'AVERAGEX(FILTER(ProductPositioning, NOT ISBLANK(ProductPositioning[battery_capacity_kwh])), ProductPositioning[battery_capacity_kwh])',
         "#,##0.00"),
        ("Average Certified Range",
         'AVERAGEX(FILTER(ProductPositioning, NOT ISBLANK(ProductPositioning[range_km])), ProductPositioning[range_km])',
         "#,##0.0"),
        ("Average Top Speed",
         'AVERAGEX(FILTER(CompetitiveAnalysis, NOT ISBLANK(CompetitiveAnalysis[top_speed_kmph])), CompetitiveAnalysis[top_speed_kmph])',
         "#,##0.0"),
        ("Average Motor Power",
         'AVERAGEX(FILTER(CompetitiveAnalysis, NOT ISBLANK(CompetitiveAnalysis[motor_power_kw])), CompetitiveAnalysis[motor_power_kw])',
         "#,##0.0"),
        ("Average Price per KM",
         'AVERAGEX(FILTER(PricingAnalysis, NOT ISBLANK(PricingAnalysis[price_per_km])), PricingAnalysis[price_per_km])',
         "#,##0.0"),
        ("Average Price per KWh",
         'AVERAGEX(FILTER(PricingAnalysis, NOT ISBLANK(PricingAnalysis[price_per_kwh])), PricingAnalysis[price_per_kwh])',
         "#,##0"),
        ("Weighted Fleet Energy Efficiency",
         'DIVIDE(SUMX(FILTER(ProductPositioning, NOT ISBLANK(ProductPositioning[range_km]) && NOT ISBLANK(ProductPositioning[battery_capacity_kwh])), ProductPositioning[range_km] * ProductPositioning[battery_capacity_kwh]), SUMX(FILTER(ProductPositioning, NOT ISBLANK(ProductPositioning[range_km]) && NOT ISBLANK(ProductPositioning[battery_capacity_kwh])), ProductPositioning[battery_capacity_kwh]), BLANK())',
         "#,##0.0"),
        ("Budget Product Count",
         'COUNTROWS(FILTER(ProductPositioning, ProductPositioning[price_bucket] = "Budget (<Rs1L)"))',
         "#,##0"),
        ("Mid-Market Product Count",
         'COUNTROWS(FILTER(ProductPositioning, ProductPositioning[price_bucket] = "Mid-Market (Rs1L-Rs1.5L)"))',
         "#,##0"),
        ("Premium Product Count",
         'COUNTROWS(FILTER(ProductPositioning, ProductPositioning[price_bucket] = "Premium (>Rs1.5L)"))',
         "#,##0"),
        ("Short-Range Product Count",
         'COUNTROWS(FILTER(ProductPositioning, ProductPositioning[range_bucket] = "Short Range (<100km)"))',
         "#,##0"),
        ("Standard-Range Product Count",
         'COUNTROWS(FILTER(ProductPositioning, ProductPositioning[range_bucket] = "Standard Range (100-150km)"))',
         "#,##0"),
        ("Long-Range Product Count",
         'COUNTROWS(FILTER(ProductPositioning, ProductPositioning[range_bucket] = "Long Range (>150km)"))',
         "#,##0"),
        ("High-Performance Product Count",
         'COUNTROWS(FILTER(CompetitiveAnalysis, CompetitiveAnalysis[top_speed_kmph] >= 100))',
         "#,##0"),
        ("Products Above Market Average",
         'COUNTROWS(FILTER(PricingAnalysis, NOT ISBLANK(PricingAnalysis[price]) && PricingAnalysis[price] > [Market Benchmark Average Price]))',
         "#,##0"),
        ("Products Below Market Average",
         'COUNTROWS(FILTER(PricingAnalysis, NOT ISBLANK(PricingAnalysis[price]) && PricingAnalysis[price] <= [Market Benchmark Average Price]))',
         "#,##0"),
        # Pending/fail-closed measures
        ("Market Registration Total [PENDING]", "BLANK()", "#,##0"),
        ("Top State Market Share [PENDING]", "BLANK()", "#,##0.0"),
        ("YoY Market Growth Rate [PENDING]", "BLANK()", "#,##0.0"),
        ("Market Penetration Rate [PENDING]", "BLANK()", "#,##0.0"),
        ("OEM Market Share [PENDING]", "BLANK()", "#,##0.0"),
        ("State Adoption Index [PENDING]", "BLANK()", "#,##0.0"),
        ("Cost Per Acquisition [PENDING]", "BLANK()", "#,##0"),
        ("Fleet Total Cost of Ownership [PENDING]", "BLANK()", "#,##0"),
    ]

    model = {
        "compatibilityLevel": 1605,
        "model": {
            "annotations": [
                {"name": "PBI_QueryOrder", "value": '["CompetitiveAnalysis","PricingAnalysis","ProductPositioning","KPIStatus","PendingMarketRegistrations"]'},
                {"name": "__PBI_TimeIntelligenceEnabled", "value": "1"},
                {"name": "PBIDesktopVersion", "value": "2.157.1354.0"},
            ],
            "culture": "en-US",
            "dataAccessOptions": {"legacyRedirects": True, "returnErrorValuesAsNull": True},
            "defaultPowerBIDataSourceVersion": "powerBI_V3",
            "sourceQueryCulture": "en-IN",
            "tables": [
                {
                    "name": "CompetitiveAnalysis",
                    "columns": cols_from_spec(comp_cols),
                    "partitions": [
                        make_csv_partition(
                            "CompetitiveAnalysis-part1",
                            "sql_competitive_analysis.csv",
                            comp_cols, 18
                        )
                    ],
                },
                {
                    "name": "PricingAnalysis",
                    "columns": cols_from_spec(pricing_cols),
                    "partitions": [
                        make_csv_partition(
                            "PricingAnalysis-part1",
                            "sql_pricing_analysis.csv",
                            pricing_cols, 17
                        )
                    ],
                },
                {
                    "name": "ProductPositioning",
                    "columns": cols_from_spec(pos_cols),
                    "partitions": [
                        make_csv_partition(
                            "ProductPositioning-part1",
                            "sql_product_positioning.csv",
                            pos_cols, 18
                        )
                    ],
                },
                {
                    "name": "KPIStatus",
                    "columns": cols_from_spec(kpi_cols),
                    "partitions": [
                        make_csv_partition(
                            "KPIStatus-part1",
                            "sql_kpi_results.csv",
                            kpi_cols, 7
                        )
                    ],
                },
                {
                    "name": "PendingMarketRegistrations",
                    "annotations": [
                        {"name": "DATA_STATUS", "value": "PENDING_VERIFIED_VAHAN_DATA"}
                    ],
                    "columns": [
                        {"name": "_placeholder", "dataType": "int64",
                         "sourceColumn": "_placeholder", "isHidden": True}
                    ],
                    "partitions": [
                        {
                            "name": "PendingMarketRegistrations-part1",
                            "mode": "import",
                            "source": {
                                "type": "m",
                                "expression": [
                                    "let",
                                    '    Source = #table(',
                                    '        type table [_placeholder = Int64.Type],',
                                    '        {}',
                                    '    )',
                                    "in",
                                    "    Source",
                                ],
                            },
                        }
                    ],
                },
                {
                    "name": "_Measures",
                    "columns": [
                        {"name": "_placeholder", "dataType": "int64",
                         "sourceColumn": "_placeholder", "isHidden": True}
                    ],
                    "measures": [
                        {
                            "name": name,
                            "expression": expr,
                            "formatString": fmt,
                            "annotations": [
                                {"name": "VERIFIED",
                                 "value": "FALSE" if "PENDING" in name else "TRUE"}
                            ],
                        }
                        for name, expr, fmt in measures
                    ],
                    "partitions": [
                        {
                            "name": "_Measures-part1",
                            "mode": "import",
                            "source": {
                                "type": "m",
                                "expression": [
                                    "let",
                                    "    Source = #table(type table [_placeholder = Int64.Type], {})",
                                    "in",
                                    "    Source",
                                ],
                            },
                        }
                    ],
                },
            ],
            "relationships": [],
            "roles": [],
        },
    }

    return model


if __name__ == "__main__":
    model = build_model()
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(model, f, indent=2, ensure_ascii=False)
    print("model.bim generated successfully at:")
    print(" ", OUTPUT)
    # Also write to non-definition path for root-level PBIP compatibility
    root_output = os.path.join(REPO_ROOT, "powerbi",
                               "Market-Business-Strategy-Intelligence.SemanticModel",
                               "model.bim")
    with open(root_output, "w", encoding="utf-8") as f:
        json.dump(model, f, indent=2, ensure_ascii=False)
    print(" ", root_output)
    # Validate it can be parsed back
    with open(OUTPUT, "r", encoding="utf-8") as f:
        check = json.load(f)
    tables = check["model"]["tables"]
    measures = next(t for t in tables if t["name"] == "_Measures")
    print("Tables:", [t["name"] for t in tables])
    print("DAX measures:", len(measures["measures"]))
    print("Pending BLANK() measures:", sum(1 for m in measures["measures"] if m["expression"] == "BLANK()"))
    print("JSON is valid: YES")
