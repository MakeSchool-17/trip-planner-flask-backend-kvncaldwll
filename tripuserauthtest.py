import tripplanner
import unittest
import json
from pymongo import MongoClient


if __name__ == '__main__':
import tripplanner
import unittest
import json
from pymongo import MongoClient
import bcrypt


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

        def test_posting_user(self):
            import pdb; pdb.set_trace()
            password = 'password123'
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt(12))
            user = {'username': 'keivnc', 'password': hashed_password}
            response = self.app.post('/users/', data=json.dumps(dict(user)), content_type='application/json')
            responseJSON = json.loads(response.data.decode())
            userID = responseJSON['_id']
            self.assertEqual(response.status_code, 200)
            assert 'application/json' in response.content_type
            assert 'keivnc' in responseJSON["username"]
            assert hashed_password in responseJSON["password"]

if __name__ == '__main__':
    unittest.main()
    unittest.main()
