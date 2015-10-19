import tripplanner
import unittest
import json
from pymongo import MongoClient
import bcrypt
import pickle


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
        new_username = "kevin"
        new_password = 'password123'
        encode_pass = new_password.encode("utf-8")
        hashed_password = bcrypt.hashpw(encode_pass, bcrypt.gensalt(12))
        response = self.app.post('/users/', data=json.dumps(dict(username=new_username, password=hashed_password)), content_type='application/json')
        responseJSON = json.loads(response.data.decode())
        userID = responseJSON['_id']
        self.assertEqual(response.status_code, 200)
        assert 'application/json' in response.content_type
        assert 'keivnc' in responseJSON["username"]
        assert hashed_password in responseJSON["password"]

if __name__ == '__main__':
    unittest.main()
    unittest.main()
