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
        db.drop_collection('users')
        db.drop_collection('trips')


    def test_posting_user(self):
        response = self.app.post('/users/', data=json.dumps(dict(username='admin', password='secret')), content_type='application/json')
        responseJSON = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        assert 'application/json' in response.content_type
        return responseJSON

    def post_with_auth(self):
        response = self.app.post('/trips/', data=json.dumps(dict(trip='europe', waypoints=['london', 'paris', 'milan'])), content_type='application/json', header=('admin', 'secret'))
        responseJSON = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        assert 'application/json' in response.content_type
        return responseJSON

if __name__ == '__main__':
    unittest.main()
    unittest.main()
