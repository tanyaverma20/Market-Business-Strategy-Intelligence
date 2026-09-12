import unittest
import pandas as pd
from data_processing import STATES, standardise_states


class StateStandardisationTests(unittest.TestCase):
    def test_legacy_alias_and_code_are_standardised(self):
        report = {"errors": []}
        actual = standardise_states(pd.DataFrame({"state": ["Orissa"], "state_code": ["OD"]}), report)
        self.assertEqual(actual.loc[0, "state"], "Odisha")
        self.assertEqual(actual.loc[0, "state_code"], STATES["Odisha"])
        self.assertEqual(report["errors"], ["state code mismatch: 1 rows"])


if __name__ == "__main__":
    unittest.main()
