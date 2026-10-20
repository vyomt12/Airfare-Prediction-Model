from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from server import create_app, FarePredictor, predict_fare, Route, STEPS
import numpy as np


class WebTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()

    def test_home_and_assets(self):
        for path in ['/', '/static/style.css', '/static/app.js']:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                response.close()
        page = self.client.get('/')
        self.assertIn(b'Original Python model', page.data)
        self.assertNotIn(b'$37.90', page.data)
        page.close()

    def test_metadata(self):
        data = self.client.get('/api/routes').get_json()
        self.assertIn('LAX', data['routes']['ATL'])
        self.assertEqual(data['records'], 249884)

    def test_api_matches_original_model_for_every_quarter(self):
        values = []
        for quarter in range(1, 5):
            with self.subTest(quarter=quarter):
                route = Route(2027, quarter, 'ATL', 'LAX', 0, 0, 0, 0, 0)
                predictor = FarePredictor(route)
                predictor.find_similar_routes()
                self.assertTrue(all(r.get_quarter() == quarter for r in predictor.route_list))
                for step in STEPS:
                    getattr(predictor, step)()
                expected = float(np.asarray(predict_fare(route)).item())
                response = self.client.post('/api/predict', json=dict(origin='ATL', destination='LAX', year=2027, quarter=quarter))
                self.assertEqual(response.status_code, 200)
                result = response.get_json()
                self.assertAlmostEqual(result['estimate'], expected, places=9)
                self.assertEqual(result['count'], len(predictor.route_list))
                self.assertEqual(result['count'], len(result['history']))
                values.append(result['estimate'])
        self.assertNotEqual(values[0], values[1])

    def test_input_validation(self):
        valid = dict(origin='ATL', destination='LAX', year=2027, quarter=1)
        for change in [dict(quarter=0), dict(quarter=True), dict(year=2027.5), dict(origin='Atlanta'), dict(destination='ATL')]:
            with self.subTest(change=change):
                response = self.client.post('/api/predict', json=valid | change)
                self.assertEqual(response.status_code, 400)
                self.assertIn('error', response.get_json())
        self.assertEqual(self.client.post('/api/predict', json=[]).status_code, 400)

    def test_missing_route_is_a_form_error(self):
        response = self.client.post('/api/predict', json=dict(origin='XXX', destination='YYY', year=2027, quarter=1))
        self.assertEqual(response.status_code, 422)
        self.assertIn('No historical records', response.get_json()['error'])



if __name__ == '__main__':
    unittest.main()
