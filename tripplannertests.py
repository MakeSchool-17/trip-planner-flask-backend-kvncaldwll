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
        # [Ben-G] You should also drop the user collection to make sure that you always
        # start without users. Each test should set up the entire environment it needs.
        # This way the tests don't depend on each other and are guaranteed to verify
        # the tested code correctly.

    # Users testing

    def test_posting_user(self):
        import pdb; pdb.set_trace()
        username = 'kevin'
        response = self.app.post('/users/', data=json.dumps(dict(user=username)), content_type='application/json')
        post_responseJSON = json.loads(response.data.decode())
        postedUserID = post_responseJSON["_id"]
        self.assertEqual(response.status_code, 200)
        assert 'application/json' in response.content_type
        assert 'kevin' in responseJSON["user"]

    # Trips tests

    def test_posting_trip(self):
        my_trip = [{'user_id': '012345'}, {'trip': 'caribbean'}, {'waypoints': ['puerto rico', 'dominican republic', 'jamaica']}]
        response = self.app.post('/trips/', data=json.dumps(dict(trip=my_trip)), content_type='application/json')
        post_responseJSON = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        assert 'application/json' in response.content_type

    def test_updating_trip(self):
        my_trip = [{'trip': 'africa'}, {'waypoints': ['ethiopia', 'egypt', 'south africa']}]
        response = self.app.post('/trips/', data=json.dumps(dict(trip=my_trip)), content_type='application/json')
        post_responseJSON = json.loads(response.data.decode())
        # var holds trip_id
        postedObjectID = post_responseJSON["_id"]
        self.assertEqual(response.status_code, 200)

        # update value at trip_id (postedObjectID)
        my_trip = [{'trip': 'africa'}, {'waypoints': ['ethiopia', 'egypt', 'south africa', 'congo']}]
        update = self.app.put('/trips/'+postedObjectID, data=json.dumps(dict(trip=my_trip)), content_type='application/json')
        update_responseJSON = json.loads(update.data.decode())
        # confirm updated value is matched
        self.assertEqual(update.status_code, 200)

    def test_deleting_trip(self):
        # post new trip
        my_trip = [{'trip': 'europe'}, {'waypoints': ['greece', 'france', 'italy', 'germany']}]
        # [Ben-G] For deletion it is not necessary to pass a body to the server, an ID is sufficient
        response = self.app.post('/trips/', data=json.dumps(dict(trip=my_trip)), content_type='application/json')
        post_responseJSON = json.loads(response.data.decode())
        postedObjectID = post_responseJSON["_id"]
        self.assertEqual(response.status_code, 200)

        # delete post by trip_id
        delete_response = self.app.delete('/trips/'+postedObjectID)
        delete_checkJSON = json.loads(delete_response.data.decode())
        self.assertEqual(delete_response.status_code, 200)
        get_deleted = self.app.get('/trips/'+postedObjectID)
        get_deleted_responseJSON = json.loads(get_deleted.data.decode())
        self.assertEqual(get_deleted.status_code, 404)


if __name__ == '__main__':
    unittest.main()
