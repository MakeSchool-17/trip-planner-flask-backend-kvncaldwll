import tripplanner
import unittest
import json
from pymongo import MongoClient


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.app = tripplanner.app.test_client()
        # Run app in testing mode to retrieve exceptions and stack traces
        tripplanner.app.config['TESTING'] = True

        # Inject test database into application
        mongo = MongoClient('localhost', 27017)
        db = mongo.test_database
        tripplanner.app.db = db

        # Drop collection (significantly faster than dropping entire db)
        db.drop_collection('trips')

    # MyObject tests

    def test_posting_trip(self):
        response = self.app.post('/trips/', data=json.dumps(dict(trip="murica")), content_type='application/json')
        responseJSON = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        assert 'application/json' in response.content_type
        assert 'murica' in responseJSON["trips"]

    def test_getting_trip(self):
        response = self.app.post('/trips/', data=json.dumps(dict(trip="egypt")), content_type='application/json')

        postResponseJSON = json.loads(response.data.decode())
        postedObjectID = postResponseJSON["_id"]

        response = self.app.get('/trips/'+postedObjectID)
        responseJSON = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        assert 'egypt' in responseJSON["trip"]

    def test_getting_non_existent_trip(self):
        response = self.app.get('/trips/55f0cbb4236f44b7f0e3cb23')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
