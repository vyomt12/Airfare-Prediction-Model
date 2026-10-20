# Airfare Prediction Model

A Python airfare prediction project with a web interface built using HTML, CSS, JavaScript, and Flask. Select an airport pair, year, and travel quarter to get an estimate from the original Python model.

## Run the web interface

```bash
cd PythonProject
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-web.txt
python server.py
```

Open http://127.0.0.1:8765/ in your browser. On Windows, activate the virtual environment with `.venv\Scripts\activate`. The server is intended for local use.

In PyCharm, select your project's `.venv` interpreter and run `PythonProject/server.py`.

## Project files

- `PythonProject/FarePredictor.py`: original regression models and final-fare calculation, with quarter filtering.
- `PythonProject/Route.py`: route data and accessors.
- `PythonProject/main.py`: original command-line entry point.
- `PythonProject/server.py`: Flask adapter that calls the original prediction workflow.
- `PythonProject/static/`: HTML page, CSS styles, and JavaScript interactions.
- `PythonProject/data.csv`: existing historical dataset.
- `PythonProject/tests/test_web.py`: API and integration checks.

## Check the web integration

From `PythonProject`:

```bash
python -m unittest discover -s tests -v
```

Tests compare the API with direct calls to the original model for each quarter, validate inputs, and check that page assets are served.

## Scope

The web layer uses the existing prediction formulas. JavaScript handles the form and calls Flask; it does not implement a replacement model. Quarter selection restricts the historical route records to the selected quarter.

The model uses all matching years in the dataset. Estimates are not live ticket quotes, and this repository does not claim validated forecasting accuracy.
