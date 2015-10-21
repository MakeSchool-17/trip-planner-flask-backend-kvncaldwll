import tripplanner
import unittest
import json
from pymongo import MongoClient
import base64


def auth_header(username, password):
    credentials = '{0}:{1}'.format(username, password).encode('utf-8')
    encode_login = base64.b64encode(credentials).decode()
    return dict(Authorization="Basic " + encode_login)


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

    def test_post_user(self):
        response = self.app.post('/users/',
                                data=json.dumps(dict(username='admin',
                                password='secret')),
                                content_type='application/json')
        responseJSON = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        assert 'application/json' in response.content_type
        return responseJSON

    def test_post_trip_auth(self):
        # import pdb; pdb.set_trace()
        trip_data = dict(trip='europe', waypoints=['london', 'paris', 'milan'])
        response = self.app.post('/trips/',
                                 data=json.dumps(trip_data),
                                 content_type='application/json',
                                 headers=auth_header('admin', 'secret'))
        responseJSON = json.loads(response.data.decode())
        print(responseJSON)
        self.assertEqual(response.status_code, 200)
        assert 'application/json' in response.content_type


if __name__ == '__main__':
    unittest.main()
    unittest.main()
