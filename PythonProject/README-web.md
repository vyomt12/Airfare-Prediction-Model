# Web interface

The web interface calls your existing Python prediction model through Flask.

## Files

- `server.py`: Flask server; imports your original model.
- `static/index.html`: page and fare form.
- `static/style.css`: appearance and responsive layout.
- `static/app.js`: dropdowns, quarter selection, and requests to Python.
- `requirements-web.txt`: dependencies.

## Run in PyCharm

Select the project's `.venv` interpreter, open `server.py`, and click Run. Open http://127.0.0.1:8765/ in your browser. Stop the server with PyCharm's Stop button.

If dependencies are missing, install them using the project's terminal:

```bash
python -m pip install -r requirements-web.txt
```

The Flask development server is intended for local use.

Your original `FarePredictor.py`, `Route.py`, `main.py`, and `data.csv` are unchanged by this addition. Predictions follow the original seven regression steps and final calculation, including the approved quarter filter. There is no prediction model in JavaScript.
