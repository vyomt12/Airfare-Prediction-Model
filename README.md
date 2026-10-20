# Airfare Prediction Model

A Python command-line project for exploring historical airfare trends with NumPy and scikit-learn. Enter an airport pair, quarter, and year to estimate its average fare using a route-specific linear regression baseline.

This is a learning project for applied regression and working with tabular data. It estimates historical average fares, not current ticket prices.

## How it works

1. Read the CSV by column name and validate the required fields.
2. Select records for the requested airport pair and quarter.
3. Use only years earlier than the requested year.
4. Fit a linear regression of average fare on year and return the estimate.

The quarter selects the historical observations; it is not a learned categorical coefficient. Airport order matches the stored dataset order. If a pair is unavailable, try reversing the airport codes. At least two distinct earlier years are required.

## Setup

Tested with Python 3.12.6, NumPy 2.2.4, and scikit-learn 1.6.1.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows, activate with `.venv\Scripts\activate` instead.

## Run

```bash
python main.py --year 2025 --quarter 1 --origin ATL --destination LAX
```

Example using the included data:

```text
Estimated average fare for ATL → LAX, Q1 2025: $268.69
Based on 31 earlier records for the same quarter.
Historical trend estimate; not a live ticket quote.
```

Run `python main.py` for interactive prompts. Use `--data /path/to/data.csv` to supply another dataset. Airport inputs are three-letter codes, such as ATL and LAX, rather than city names.

## Dataset

The project's existing `data.csv` contains 249,884 records spanning 1993–2024. The original download URL and redistribution license were not recorded in the project; this README does not claim a verified external source or license for the data.

Required columns:

| Column | Meaning |
| --- | --- |
| `Year` | Observation year |
| `quarter` | Quarter, 1–4 |
| `airport_1` | First airport code |
| `airport_2` | Second airport code |
| `fare` | Historical average fare in USD |

The file also contains `large_ms`, `fare_lg`, `lf_ms`, and `fare_low`. The current baseline does not use these carrier statistics. Invalid required values are skipped and counted. Missing unused carrier statistics do not invalidate an otherwise usable fare record.

## Evaluation

```bash
python evaluate.py --data data.csv --test-year 2023
```

The evaluation holds out 2023 and trains only on earlier years for each airport pair and quarter. Both methods are evaluated on the same eligible observations.

| Measure | Result |
| --- | ---: |
| 2023 holdout records | 7,788 |
| Records with sufficient history and a valid regression estimate | 7,696 |
| Linear trend mean absolute error | $37.90 |
| Last observed same-quarter fare mean absolute error | $34.27 |

Lower error is better. The last-observed-fare baseline performed better in this holdout. These results describe this dataset and split; they do not establish general predictive accuracy. Records without sufficient earlier history or with invalid extrapolations are excluded, so the error figures should be read alongside coverage.

## Tests

```bash
python -m unittest discover -s tests -v
```

Seven tests cover column mapping, quarter selection, prevention of future-data leakage, input validation, missing routes, invalid fares, and invalid extrapolations.

## Project structure

- `main.py`: interactive and argument-based CLI
- `Route.py`: validated prediction inputs
- `FarePredictor.py`: CSV loading and linear trend prediction
- `evaluate.py`: temporal holdout and baseline comparison
- `tests/`: regression and validation tests

## Limitations and next steps

A linear time trend cannot capture every change in airline pricing. This model does not incorporate booking lead time, fuel costs, holidays, inflation, or live availability, and it does not provide confidence intervals. Long-range extrapolations are particularly uncertain.

Future work could compare rolling training windows, seasonal features, and nonlinear models using separate validation periods before evaluating on an untouched final holdout.

## Maintenance update

The initial implementation combined separately predicted carrier fares and market shares. This revision fixes the CSV column mapping and replaces that calculation with a direct average-fare regression baseline. It also adds quarter filtering, validation, reproducible evaluation, and tests. The original implementation remains in Git history.
