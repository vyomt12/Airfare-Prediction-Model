"""Validated inputs for an airport-pair fare estimate."""
from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Route:
    year: int
    quarter: int
    origin: str
    destination: str

    def __post_init__(self):
        if not 1 <= self.year <= 9999:
            raise ValueError("Year must be between 1 and 9999.")
        if self.quarter not in (1, 2, 3, 4):
            raise ValueError("Quarter must be 1, 2, 3, or 4.")
        for name in ("origin", "destination"):
            code = getattr(self, name).strip().upper()
            if not re.fullmatch(r"[A-Z]{3}", code):
                raise ValueError("Enter three-letter airport codes, such as ATL or LAX.")
            object.__setattr__(self, name, code)
        if self.origin == self.destination:
            raise ValueError("Origin and destination must be different airports.")
