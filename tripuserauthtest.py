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

    def test_userdb(self):
        response = self.app.post('/users/',
                                data=json.dumps(dict(username='admin',
                                password='secret')),
                                content_type='application/json')
        responseJSON = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        print(responseJSON)

        trip_data = dict(trip='africa', waypoints=['egypt', 'ethiopia', 'south africa'])
        response = self.app.post('/trips/',
                                 data=json.dumps(trip_data),
                                 content_type='application/json',
                                 headers=auth_header('admin', 'secret'))
        responseJSON = json.loads(response.data.decode())
        postedObjectID = responseJSON['_id']
        self.assertEqual(response.status_code, 200)
        print(responseJSON)

        response = self.app.get('users/'+postedObjectID,
                                headers=auth_header('admin', 'secret'))
        responseJSON = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        print(responseJSON)


    def test_tripdb_auth(self):
        # create new user
        response = self.app.post('/users/',
                                data=json.dumps(dict(username='admin',
                                password='secret')),
                                content_type='application/json')
        responseJSON = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)

        # post new trip with auth
        trip_data = dict(trip='europe', waypoints=['london', 'paris', 'milan'])
        response = self.app.post('/trips/',
                                 data=json.dumps(trip_data),
                                 content_type='application/json',
                                 headers=auth_header('admin', 'secret'))
        responseJSON = json.loads(response.data.decode())
        postedObjectID = responseJSON['_id']
        self.assertEqual(response.status_code, 200)
        print(responseJSON)

        # update existing trip with auth
        up_data = dict(trip='europe', waypoints=['brussels', 'paris', 'amsterdam'])
        response = self.app.put('trips/'+postedObjectID,
                                data=json.dumps(up_data),
                                content_type='application/json',
                                headers=auth_header('admin', 'secret'))
        responseJSON = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        print(responseJSON)

        # get existing trip with auth
        response = self.app.get('trips/'+postedObjectID,
                                headers=auth_header('admin', 'secret'))
        responseJSON = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        print(responseJSON)

        # get non existing trip
        response = self.app.get('trips/57389d84496254540367aa0d',
                                headers=auth_header('admin', 'secret'))
        responseJSON = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        print(responseJSON)

        # delete trip with auth
        response = self.app.delete('trips/'+postedObjectID,
                                headers=auth_header('admin', 'secret'))
        self.assertEqual(response.status_code, 200)
        print(responseJSON)

        # delete non existing trip
        response = self.app.delete('trips/68389d84496254540367aa0d',
                                headers=auth_header('admin', 'secret'))
        self.assertEqual(response.status_code, 200)
        print(responseJSON)

        # get deleted trip
        response = self.app.get('trips/'+postedObjectID,
                                headers=auth_header('admin', 'secret'))
        self.assertEqual(response.status_code, 404)
        print(responseJSON)


if __name__ == '__main__':
    unittest.main()
    unittest.main()
