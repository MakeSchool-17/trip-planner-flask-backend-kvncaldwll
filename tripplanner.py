from flask import Flask, request, make_response, jsonify
from flask_restful import Resource, Api
from pymongo import MongoClient
from bson.objectid import ObjectId
from utils.mongo_json_encoder import JSONEncoder
from json import dumps

app = Flask(__name__)
mongo = MongoClient('localhost', 27017)
app.db = mongo.develop_database
api = Api(app)


class Trips(Resource):
    # add a new trip
    def post(self):
        new_trip = request.json
        trip_collection = app.db.my_trips
        result = trip_collection.insert_one(new_trip)
        my_trip = trip_collection.find_one({'_id': ObjectId(result.inserted_id)})
        return my_trip

    # find trip by trip_id or return all trips in db
    def get(self, trip_id=None):
        trip_collection = app.db.my_trips
        if trip_id is not None:
            my_trip = trip_collection.find_one({'_id': ObjectId(trip_id)})
            if my_trip is None:
                response = jsonify(data=[])
                response.status_code = 404
                return response
            else:
                return my_trip
        else:
            my_trip = trip_collection.find()
            return dumps(my_trip)

    # find trip_id, update data
    def put(self, trip_id):
        update_trip = request.json
        trip_collection = app.db.my_trips
        my_trip = trip_collection.find_one({'_id': ObjectId(trip_id)})
        if my_trip is None:
            response = jsonify(data=[])
            response.status_code = 404
            return response
        else:
            update_trip = trip_collection.update_one({'_id': ObjectId(trip_id)}, {'$set': update_trip}, upsert=False)
            mod_trip = trip_collection.find_one({'_id': ObjectId(trip_id)})
            return mod_trip

    # remove trip by trip_id
    def delete(self, trip_id):
        trip_collection = app.db.my_trips
        remove_trip = trip_collection.remove(ObjectId(trip_id))
        if remove_trip is None:
            response = jsonify(data=[])
            response.status_code = 404
            return response


class Users(Resource):
    # add new user to db
    def post(self):
        new_user = request.json
        user_collection = app.db.users
        result = user_collection.insert_one(new_user)
        my_user = user_collection.find_one({'_user': ObjectId(result.inserted_id)})
        return my_user

    # find trips for user
    def get(self, user_id):
        user_collection = app.db.users
        my_user = user_collection.find_one({'_user': ObjectId(user_id)})
        if my_user is None:
            response = jsonify(data=[])
            response.status_code = 404
            return response
        else:
            user_trips = user_collection.find()
            return dumps(user_trips)

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
