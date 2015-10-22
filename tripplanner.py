from flask import Flask, request, make_response, jsonify
from flask_restful import Resource, Api
from pymongo import MongoClient
from bson.objectid import ObjectId
from utils.mongo_json_encoder import JSONEncoder
from json import dumps
import bcrypt
from functools import wraps

app = Flask(__name__)
mongo = MongoClient('localhost', 27017)
app.db = mongo.develop_database
api = Api(app)
app.bcrypt_rounds = 12


def check_auth(username, password):
    user_db = app.db.users
    find_username = user_db.find_one({'username': username})
    if find_username is None:
        message = {'error': 'User Not Found'}
        response = jsonify(message)
        response.status_code = 404
        return response
    else:
        encode_pass = password.encode('utf-8')
        hashed_password = bcrypt.hashpw(encode_pass, )
        return True
    # return username == 'admin' and password == 'secret'


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            message = {'error': 'Basic Auth Required.'}
            resp = jsonify(message)
            resp.status_code = 401
            return resp
        return f(*args, **kwargs)
    return decorated


class Trips(Resource):
    @requires_auth
    def post(self):
        username = request.authorization.username
        new_trip = request.json
        new_trip["username"] = username
        trip_db = app.db.trips
        result = trip_db.insert_one(new_trip)
        my_trip = trip_db.find_one({'_id': ObjectId(result.inserted_id)})
        return my_trip

    @requires_auth
    def get(self, trip_id=None):
        trip_db = app.db.trips
        if trip_id is not None:
            my_trip = trip_db.find_one({'_id': ObjectId(trip_id)})
            if my_trip is None:
                response = jsonify(data=[])
                response.status_code = 404
                return response
            else:
                return my_trip
        else:
            my_trip = trip_db.find()
            return dumps(my_trip)

    @requires_auth
    def put(self, trip_id):
        update_trip = request.json
        trip_db = app.db.trips
        my_trip = trip_db.find_one({'_id': ObjectId(trip_id)})
        if my_trip is None:
            response = jsonify(data=[])
            response.status_code = 404
            return response
        else:
            update_trip = trip_db.update_one({'_id': ObjectId(trip_id)}, {'$set': update_trip}, upsert=False)
            mod_trip = trip_db.find_one({'_id': ObjectId(trip_id)})
            return mod_trip

    @requires_auth
    def delete(self, trip_id):
        trip_db = app.db.trips
        remove_trip = trip_db.delete_one({'_id': ObjectId(trip_id)})
        if remove_trip is None:
            response = jsonify(data=[])
            response.status_code = 404
            return response


class Users(Resource):
    def post(self):
        new_user = request.json
        username_db = app.db.users
        encode_pass = new_user['password'].encode('utf-8')
        hashed_password = bcrypt.hashpw(encode_pass, bcrypt.gensalt(app.bcrypt_rounds))
        new_user['password'] = hashed_password
        result = username_db.insert_one(new_user)
        user = username_db.find_one({'_id': ObjectId(result.inserted_id)})
        # dont return hashed passowrds to anyone!!!
        del user['password']
        return user

    @requires_auth
    def get(self):
        username = request.authorization.username
        trip_db = app.db.trips
        user_trips = trip_db.find(username)
        if user_trips is None:
            response = jsonify(data=[])
            response.status_code = 404
            return response
        else:
            return dumps()


api.add_resource(Trips, '/trips/', '/trips/<string:trip_id>')
api.add_resource(Users, '/users/', '/users/<string:user_id>')


@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(JSONEncoder().encode(data), code)
    resp.headers.extend(headers or {})
    return resp

if __name__ == '__main__':
    app.config['TRAP_BAD_REQUEST_ERRORS'] = True
    app.run(debug=True)
