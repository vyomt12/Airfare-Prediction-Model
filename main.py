"""Command-line interface; run with --help for options."""
import argparse
from pathlib import Path

from FarePredictor import FarePredictor
from Route import Route


def main():
    parser = argparse.ArgumentParser(description="Estimate a historical airport-pair average fare trend.")
    parser.add_argument("--data", type=Path, default=Path(__file__).with_name("data.csv"))
    parser.add_argument("--year", type=int)
    parser.add_argument("--quarter", type=int)
    parser.add_argument("--origin", help="Three-letter airport code, e.g. ATL")
    parser.add_argument("--destination", help="Three-letter airport code, e.g. LAX")
    args = parser.parse_args()
    try:
        route = Route(
            args.year if args.year is not None else int(input("Year: ")),
            args.quarter if args.quarter is not None else int(input("Quarter (1-4): ")),
            args.origin if args.origin is not None else input("Origin airport code: "),
            args.destination if args.destination is not None else input("Destination airport code: "),
        )
        predictor = FarePredictor(args.data)
        fare = predictor.predict(route)
        print(f"Estimated average fare for {route.origin} → {route.destination}, "
              f"Q{route.quarter} {route.year}: ${fare:,.2f}")
        print(f"Based on {len(predictor.history(route))} earlier records for the same quarter.")
        print("Historical trend estimate; not a live ticket quote.")
        if predictor.skipped_rows:
            print(f"Skipped {predictor.skipped_rows} invalid dataset rows.")
    except (ValueError, OSError, EOFError) as exc:
        parser.exit(2, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
