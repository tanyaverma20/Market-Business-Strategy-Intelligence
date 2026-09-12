import tempfile
import unittest

import pandas as pd

from analytics.competitive_analysis import (
    compute_manufacturer_count,
    compute_product_count,
    compute_product_category_distribution,
    compute_price_comparison,
    compute_battery_comparison,
    compute_range_comparison,
    compute_top_speed_comparison,
    compute_motor_power_comparison,
    compute_price_per_km,
    compute_price_per_kwh,
    compute_range_realization,
    compute_manufacturer_portfolio_analysis,
    rank_products,
)
from analytics.pricing_analysis import (
    compute_ex_showroom_price,
    compute_effective_price_after_subsidy,
    compute_price_per_certified_km,
    compute_price_per_kwh,
    compute_price_percentile,
    compute_range_percentile,
    compute_battery_percentile,
    compute_value_score,
)
from analytics.positioning_analysis import classify_product_segment
from analytics.unit_economics import (
    compute_gross_margin,
    compute_contribution_margin,
    compute_contribution_margin_pct,
    compute_break_even_units,
    compute_break_even_revenue,
)
from analytics.geographic_analysis import compute_gai_template
from analytics.market_analysis import (
    market_status_for_verified_data,
    validate_required_columns,
)
from analytics.kpi_engine import generate_kpi_outputs


class TestAnalyticalEngine(unittest.TestCase):
    def setUp(self):
        self.product_df = pd.DataFrame(
            {
                "manufacturer": ["Ather", "Ather", "TVS", "TVS"],
                "model_name": ["450X", "Rizta", "iQube", "iQube ST"],
                "vehicle_category": ["electric scooter", "electric scooter", "electric scooter", "electric scooter"],
                "ex_showroom_price_inr": [150000, 130000, 120000, 170000],
                "battery_capacity_kwh": [3.7, 3.7, 3.5, 5.3],
                "certified_range_km": [161.0, 159.0, 145.0, 212.0],
                "real_world_range_km": [145.0, 150.0, 130.0, 185.0],
                "top_speed_kmh": [80, 82, 82, 82],
                "motor_peak_power_kw": [7.0, 4.0, 4.7, 6.0],
                "source_type": ["official", "official", "official", "official"],
                "verification_status": ["verified", "verified", "verified", "verified"],
            }
        )

    def test_market_status_requires_verified_data(self):
        status = market_status_for_verified_data({"required_columns": ["year", "month", "e2w_registrations"]}, pd.DataFrame())
        self.assertIn("verified data required", status["status"].lower())

    def test_validate_required_columns_catches_missing_columns(self):
        bad_df = pd.DataFrame({"year": [2025]})
        with self.assertRaises(ValueError):
            validate_required_columns(bad_df, ["year", "month"])

    def test_product_count_and_manufacturer_count(self):
        self.assertEqual(compute_product_count(self.product_df), 4)
        self.assertEqual(compute_manufacturer_count(self.product_df), 2)

    def test_category_distribution(self):
        result = compute_product_category_distribution(self.product_df)
        self.assertEqual(result.iloc[0]["product_count"], 4)
        self.assertEqual(result.iloc[0]["share_pct"], 100.0)

    def test_price_and_battery_comparison(self):
        price_stats = compute_price_comparison(self.product_df)
        battery_stats = compute_battery_comparison(self.product_df)
        self.assertIn("min", price_stats.columns)
        self.assertIn("max", battery_stats.columns)

    def test_range_realization_requires_both_ranges(self):
        result = compute_range_realization(self.product_df)
        self.assertIn("status", result.columns)

    def test_price_per_km_and_kwh(self):
        self.assertAlmostEqual(float(compute_price_per_km(self.product_df).iloc[0]["price_per_certified_km_inr"],), 931.68, places=1)
        self.assertAlmostEqual(float(compute_price_per_kwh(self.product_df).iloc[0]["price_per_kwh_inr"]), 40540.54, places=1)

    def test_pricing_metrics(self):
        ex = compute_ex_showroom_price(self.product_df)
        self.assertIn("ex_showroom_price_inr", ex.columns)
        effective = compute_effective_price_after_subsidy(self.product_df)
        self.assertIn("effective_price_after_subsidy_inr", effective.columns)
        ppk = compute_price_per_certified_km(self.product_df)
        self.assertIn("price_per_certified_km_inr", ppk.columns)
        percentile = compute_price_percentile(self.product_df)
        self.assertIn("price_percentile", percentile.columns)

    def test_positioning_classification(self):
        classified = classify_product_segment(self.product_df.iloc[0].to_dict())
        self.assertIn("segment", classified)

    def test_unit_economics(self):
        revenue = 150000
        variable_cost = 90000
        fixed_cost = 5000000
        units_sold = 100
        self.assertAlmostEqual(compute_gross_margin(revenue, variable_cost), 60000.0)
        self.assertAlmostEqual(compute_contribution_margin(revenue, variable_cost), 60000.0)
        self.assertAlmostEqual(compute_contribution_margin_pct(revenue, variable_cost), 40.0)
        self.assertAlmostEqual(compute_break_even_units(fixed_cost, revenue - variable_cost), 83.33333333333333)
        self.assertAlmostEqual(compute_break_even_revenue(fixed_cost, revenue - variable_cost, selling_price=revenue), 12500000.0)

    def test_invalid_product_values_raise_errors(self):
        invalid = self.product_df.copy()
        invalid.loc[0, "ex_showroom_price_inr"] = -1000
        with self.assertRaises(ValueError):
            compute_price_per_km(invalid)

        invalid_range = self.product_df.copy()
        invalid_range.loc[0, "certified_range_km"] = 0
        with self.assertRaises(ValueError):
            compute_price_per_km(invalid_range)

    def test_missing_columns_and_duplicates_are_handled(self):
        with self.assertRaises(ValueError):
            compute_product_count(pd.DataFrame({"manufacturer": ["Ather"]}))

        duplicate = pd.concat([self.product_df, self.product_df.iloc[[0]]], ignore_index=True)
        self.assertEqual(compute_product_count(duplicate), 4)

    def test_gai_template(self):
        template = compute_gai_template(
            pd.DataFrame(
                {
                    "state": ["State A", "State B"],
                    "market_size": [100, 50],
                    "ev_penetration": [30, 10],
                    "growth": [20, 5],
                    "purchasing_power": [70, 30],
                    "charging_infrastructure": [80, 20],
                    "policy_score": [60, 40],
                }
            )
        )
        self.assertIn("gai_score", template.columns)
        self.assertIn("priority_tier", template.columns)

    def test_rank_products_by_price_and_range(self):
        result = rank_products(self.product_df, ["ex_showroom_price_inr", "certified_range_km"])
        self.assertIn("overall_rank", result.columns)

    def test_generate_kpi_outputs_accepts_processed_schema(self):
        processed = pd.DataFrame(
            {
                "manufacturer": ["Ather", "TVS"],
                "model_name": ["450X", "iQube"],
                "vehicle_category": ["electric scooter", "electric scooter"],
                "ex_showroom_price_inr": [150000.0, 120000.0],
                "battery_capacity_kwh": [3.7, 3.5],
                "range_km": [161.0, 145.0],
                "real_world_range_km": [145.0, 130.0],
                "top_speed_kmh": [80.0, 82.0],
                "motor_peak_power_kw": [7.0, 4.7],
                "source_type": ["official", "official"],
                "verification_status": ["verified", "verified"],
            }
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            outputs = generate_kpi_outputs(processed, tmpdir)
            self.assertIn("pricing_kpis", outputs)
            self.assertTrue(pd.read_csv(f"{tmpdir}/pricing_kpis.csv").shape[0] > 0)


if __name__ == "__main__":
    unittest.main()
