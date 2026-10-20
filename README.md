# Airfare Prediction Model

A web application that estimates airfare for a selected airport pair, year, and travel quarter using historical data and linear regression.

### Features

- Select departure and destination airports from available routes.
- Filter historical records by travel quarter.
- Generate fare estimates through a Python prediction model.
- View results in a responsive web interface.

### How it works

The frontend sends the selected route, year, and quarter to a Flask API. The Python model fits regression models to historical fare and airline market-share data, then combines their outputs into a fare estimate.

### Tech stack

**Python · scikit-learn · NumPy · Flask · JavaScript · HTML · CSS**

### Evaluation

The corrected model was evaluated on **2023 fares**, using only records from **before 2023** for training and matching the airport pair and travel quarter.

| Metric | Result |
| --- | ---: |
| Mean absolute error (MAE) | $63.10 |
| Median absolute error | $34.37 |
| Predictions within 20% of the observed average fare | 66.9% |
| Last-observed-fare baseline MAE | $34.47 |

The evaluation covered **7,157 of 7,788 holdout records (91.9%)**. Another 580 records lacked at least two distinct usable training years, and 51 produced nonpositive or nonfinite model estimates. The reported errors exclude those records.

The baseline reuses the most recent earlier same-quarter average fare for each airport pair and is scored on the same evaluated records. **The baseline outperformed the model.** Some model estimates were extreme outliers, especially for routes with little usable history.

These results measure error against historical quarterly average fares, not individual ticket prices. “Within 20%” is an error threshold, not an overall accuracy score. Results from this single historical split do not establish future forecasting performance.

### Run locally

```bash
cd airfare_prediction
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-web.txt
python server.py
```

Open **http://127.0.0.1:8765/**.

### Tests

```bash
python -m unittest discover -s tests -v
```

Integration tests cover quarter-specific predictions, input validation, unavailable routes, and page delivery.

### Limitations

This is an exploratory learning project. Estimates use historical data rather than live ticket prices. The evaluation above shows that prediction quality and stability still need improvement.

Records with missing required numeric values or combined carrier shares of 100% or more are excluded because the model's remaining-share calculation is undefined or invalid for those rows.
