"""A route-specific linear trend baseline for historical average fares."""
from collections import defaultdict
import csv
from dataclasses import dataclass
from math import isfinite
from pathlib import Path

import numpy as np
from sklearn.linear_model import LinearRegression

from Route import Route


@dataclass(frozen=True)
class FareRecord:
    year: int
    quarter: int
    origin: str
    destination: str
    fare: float


class FarePredictor:
    def __init__(self, data_path: str | Path):
        self.records = []
        self.skipped_rows = 0
        self.index = defaultdict(list)
        with open(data_path, newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            required = {"Year", "quarter", "airport_1", "airport_2", "fare"}
            missing = required - set(reader.fieldnames or [])
            if missing:
                raise ValueError(f"CSV is missing required columns: {', '.join(sorted(missing))}")
            for row in reader:
                try:
                    route = Route(int(row["Year"]), int(row["quarter"]),
                                  row["airport_1"], row["airport_2"])
                    fare = float(row["fare"])
                    if not isfinite(fare) or fare <= 0:
                        raise ValueError("Fare must be finite and positive.")
                except (ValueError, TypeError, AttributeError):
                    self.skipped_rows += 1
                    continue
                record = FareRecord(route.year, route.quarter, route.origin,
                                    route.destination, fare)
                self.records.append(record)
                self.index[(record.origin, record.destination, record.quarter)].append(record)
        if not self.records:
            raise ValueError("CSV contains no usable fare records.")

    def history(self, route: Route):
        # Using only earlier years prevents future observations from leaking in.
        return [r for r in self.index[(route.origin, route.destination, route.quarter)]
                if r.year < route.year]

    def predict(self, route: Route) -> float:
        records = self.history(route)
        if len({r.year for r in records}) < 2:
            raise ValueError("Need at least two earlier years for this airport pair and quarter. "
                             "Try another route or the reverse airport order.")
        years = np.array([r.year for r in records], dtype=float).reshape(-1, 1)
        fares = np.array([r.fare for r in records], dtype=float)
        model = LinearRegression().fit(years, fares)
        prediction = float(model.predict([[route.year]])[0])
        if not isfinite(prediction) or prediction <= 0:
            raise ValueError("The fitted trend produced an invalid fare; this route needs a better model.")
        return prediction
