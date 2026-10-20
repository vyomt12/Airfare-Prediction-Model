import csv
from pathlib import Path
import tempfile
import unittest

from FarePredictor import FarePredictor
from Route import Route


class PredictionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "fares.csv"

    def write_rows(self, rows):
        with self.path.open("w", newline="") as handle:
            writer = csv.writer(handle)
            # Deliberately reorder columns to test header-based mapping.
            writer.writerow(["fare", "airport_2", "quarter", "Year", "airport_1", "large_ms"])
            writer.writerows(rows)
        return FarePredictor(self.path)

    def test_header_mapping_quarter_selection_and_future_leakage(self):
        predictor = self.write_rows([
            [100, "LAX", 1, 2020, "ATL", .7],
            [110, "LAX", 1, 2021, "ATL", .7],
            [9999, "LAX", 2, 2021, "ATL", .7],
            [9999, "LAX", 1, 2022, "ATL", .7],
            [9999, "LAX", 1, 2023, "ATL", .7],
        ])
        self.assertAlmostEqual(predictor.predict(Route(2022, 1, "atl", "lax")), 120)

    def test_insufficient_history(self):
        predictor = self.write_rows([[100, "LAX", 1, 2020, "ATL", .7]])
        with self.assertRaisesRegex(ValueError, "two earlier years"):
            predictor.predict(Route(2022, 1, "ATL", "LAX"))

    def test_unknown_route(self):
        predictor = self.write_rows([[100, "LAX", 1, 2020, "ATL", .7]])
        with self.assertRaises(ValueError):
            predictor.predict(Route(2022, 1, "JFK", "LAX"))

    def test_invalid_fares_are_skipped(self):
        predictor = self.write_rows([
            [100, "LAX", 1, 2020, "ATL", .7],
            ["nan", "LAX", 1, 2021, "ATL", .7],
            ["", "LAX", 1, 2021, "ATL", .7],
            [-1, "LAX", 1, 2021, "ATL", .7],
        ])
        self.assertEqual(predictor.skipped_rows, 3)
        self.assertEqual(len(predictor.records), 1)

    def test_missing_columns(self):
        self.path.write_text("Year,fare\n2020,100\n")
        with self.assertRaisesRegex(ValueError, "missing required columns"):
            FarePredictor(self.path)

    def test_invalid_inputs(self):
        for values in [(2025, 0, "ATL", "LAX"), (2025, 1, "Atlanta", "LAX"),
                       (2025, 1, "ATL", "ATL"), (0, 1, "ATL", "LAX")]:
            with self.subTest(values=values), self.assertRaises(ValueError):
                Route(*values)

    def test_nonpositive_extrapolation_is_rejected(self):
        predictor = self.write_rows([
            [100, "LAX", 1, 2020, "ATL", .7], [10, "LAX", 1, 2021, "ATL", .7],
        ])
        with self.assertRaisesRegex(ValueError, "invalid fare"):
            predictor.predict(Route(2023, 1, "ATL", "LAX"))


if __name__ == "__main__":
    unittest.main()
