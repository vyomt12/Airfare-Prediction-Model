"""Temporal holdout evaluation against a last-observed-fare baseline."""
import argparse
import json
from statistics import mean

from FarePredictor import FarePredictor
from Route import Route


def evaluate(data_path, test_year):
    predictor = FarePredictor(data_path)
    test_rows = [r for r in predictor.records if r.year == test_year]
    model_errors, baseline_errors = [], []
    for record in test_rows:
        route = Route(record.year, record.quarter, record.origin, record.destination)
        try:
            prediction = predictor.predict(route)
        except ValueError:
            continue
        history = predictor.history(route)
        latest_year = max(r.year for r in history)
        baseline = mean(r.fare for r in history if r.year == latest_year)
        model_errors.append(abs(prediction - record.fare))
        baseline_errors.append(abs(baseline - record.fare))
    if not model_errors:
        raise ValueError("No eligible holdout records for the selected year.")
    return {
        "test_year": test_year,
        "training_years": f"strictly before {test_year}",
        "usable_rows": len(predictor.records),
        "skipped_invalid_rows": predictor.skipped_rows,
        "holdout_rows": len(test_rows),
        "evaluated_rows": len(model_errors),
        "linear_trend_mae_usd": round(mean(model_errors), 2),
        "last_observed_fare_mae_usd": round(mean(baseline_errors), 2),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default="data.csv")
    parser.add_argument("--test-year", type=int, default=2023)
    args = parser.parse_args()
    try:
        print(json.dumps(evaluate(args.data, args.test_year), indent=2))
    except (ValueError, OSError) as exc:
        parser.exit(2, f"Error: {exc}\n")
