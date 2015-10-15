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
        post_responseJSON = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        assert 'application/json' in response.content_type
        assert 'murica' in post_responseJSON["trip"]

    def test_updating_trip(self):
        # post trip and confirm post success
        response = self.app.post('/trips/', data=json.dumps(dict(trip="neverland")), content_type='application/json')
        post_responseJSON = json.loads(response.data.decode())
        # var holds trip_id
        postedObjectID = post_responseJSON["_id"]
        self.assertEqual(response.status_code, 200)
        assert 'neverland' in post_responseJSON["trip"]

        # update value at trip_id (postedObjectID)
        update = self.app.put('/trips/'+postedObjectID, data=json.dumps(dict(trip="atlantis")), content_type='application/json')
        update_responseJSON = json.loads(update.data.decode())
        # confirm updated value is matched
        self.assertEqual(update.status_code, 200)
        assert 'atlantis' in update_responseJSON["trip"]

    def test_deleting_trip(self):
        #post new trip
        response = self.app.post('/trips/', data=json.dumps(dict(trip="the sun")), content_type='application/json')
        post_responseJSON = json.loads(response.data.decode())
        postedObjectID = post_responseJSON["_id"]
        self.assertEqual(response.status_code, 200)
        assert 'the sun' in post_responseJSON["trip"]

        # delete post by trip_id
        delete_response = self.app.delete('/trip/'+postedObjectID)
        self.assertEqual(delete_response.status_code, 200)
        check_delete = self.app.get('/trips/'+postedObjectID)
        check_responseJSON = json.loads(check_delete.data.decode())
        self.assertEqual(delete_response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
