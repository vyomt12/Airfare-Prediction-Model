from collections import defaultdict
import csv
import math
import os
from pathlib import Path
import re
import sys

import numpy as np
from flask import Flask, jsonify, request

ROOT = Path(__file__).resolve().parent
MODEL_DIR = ROOT if (ROOT / 'FarePredictor.py').exists() else ROOT / 'PythonProject'
sys.path.insert(0, str(MODEL_DIR))
from FarePredictor import FarePredictor, predict_fare
from Route import Route

STEPS = ('future_large_ms', 'future_low_ms', 'future_middle_ms',
         'future_large_fare', 'future_low_fare', 'future_middle_fare', 'future_fare')


def create_app():
    # The existing model opens 'data.csv' relative to the process directory.
    # Set that directory once at startup, rather than modifying its file handling.
    os.chdir(MODEL_DIR)
    app = Flask(__name__, static_folder=str(ROOT / 'static'), static_url_path='/static')
    app.config['MAX_CONTENT_LENGTH'] = 4096
    history_index = defaultdict(list)
    pairs = defaultdict(set)
    years = []
    record_count = 0
    with (MODEL_DIR / 'data.csv').open(newline='') as handle:
        for record in csv.DictReader(handle):
            origin, destination = record['airport_1'], record['airport_2']
            year, quarter, fare = int(record['Year']), int(record['quarter']), float(record['fare'])
            history_index[(origin, destination, quarter)].append([year, fare])
            pairs[origin].add(destination)
            years.append(year)
            record_count += 1
    metadata = {'routes': {key: sorted(value) for key, value in sorted(pairs.items())},
                'records': record_count, 'minYear': min(years), 'maxYear': max(years)}

    @app.get('/')
    def index():
        return app.send_static_file('index.html')

    @app.get('/api/routes')
    def routes():
        return jsonify(metadata)

    @app.post('/api/predict')
    def predict():
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify(error='Send an airport pair, year, and quarter.'), 400
        origin = payload.get('origin')
        destination = payload.get('destination')
        if not isinstance(origin, str) or not isinstance(destination, str):
            return jsonify(error='Choose an origin and destination airport.'), 400
        origin, destination = origin.strip().upper(), destination.strip().upper()
        if not all(re.fullmatch(r'[A-Z]{3}', code) for code in (origin, destination)) or origin == destination:
            return jsonify(error='Choose two different three-letter airport codes.'), 400
        year, quarter = payload.get('year'), payload.get('quarter')
        if type(year) is not int or not 1 <= year <= 9999:
            return jsonify(error='Choose a valid prediction year.'), 400
        if type(quarter) is not int or quarter not in (1, 2, 3, 4):
            return jsonify(error='Choose a quarter from Q1 to Q4.'), 400
        history = history_index.get((origin, destination, quarter), [])
        if not history:
            return jsonify(error='No historical records match this airport pair and quarter.'), 422
        try:
            # This is the exact workflow from the original main.py.
            customer_route = Route(year, quarter, origin, destination, 0, 0, 0, 0, 0)
            predictor = FarePredictor(customer_route)
            predictor.find_similar_routes()
            for step in STEPS:
                getattr(predictor, step)()
            estimate = float(np.asarray(predict_fare(customer_route)).item())
            if not math.isfinite(estimate) or estimate <= 0:
                raise ValueError('Nonpositive or nonfinite estimate')
        except (ValueError, ZeroDivisionError, FloatingPointError, OverflowError):
            app.logger.exception('Original model failed for %s-%s Q%s %s', origin, destination, quarter, year)
            return jsonify(error='The original model could not calculate a valid fare for this selection. Try another route or year.'), 422
        return jsonify(estimate=estimate, history=sorted(history), count=len(predictor.route_list),
                       origin=origin, destination=destination, year=year, quarter=quarter)

    return app


if __name__ == '__main__':
    create_app().run(host='127.0.0.1', port=8765, debug=False)
