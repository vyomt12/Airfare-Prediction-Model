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

### Run locally

```bash
cd PythonProject
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

This is an exploratory learning project. Estimates use historical data rather than live ticket prices, and forecasting accuracy has not been validated.
