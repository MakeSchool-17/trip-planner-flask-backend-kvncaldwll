# import dependencies for
from flask import Flask, request, make_response, jsonify
from flask_restful import Resource, Api
from pymongo import MongoClient
from bson.objectid import ObjectId
from utils.mongo_json_encoder import JSONEncoder

# create flask server, specify database, create flask_RESTful API
app = Flask(__name__)
mongo = MongoClient('localhost', 27017)
app.db = mongo.develop_database
api = Api(app)


class Trips(Resource):
    def post(self):
        new_trip = request.json
        trip_collection = app.db.my_trips
        result = trip_collection.insert_one(new_trip)
        my_trip = trip_collection.find_one({'_id': ObjectId(result.insert_id)})
        return my_trip

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
            return my_trip

    def put(self, trip_id, up_data):
        trip_collection = app.db.my_trips
        my_trip = trip_collection.find_one({'_id': ObjectId(trip_id)})
        if my_trip is None:
            response = jsonify(data=[])
            response.status_code = 404
            return response
        else:
            update_trip = trip_collection.update_one({'_id': ObjectId(trip_id)}, {'$set': up_data}, upsert=False)
            mod_trip = trip_collection.find_one({'_id': ObjectId(update_trip.insert_id)})
            return mod_trip

    def delete(self, trip_id):
        trip_collection = app.db.my_trips
        remove_trip = trip_collection.remove_one(ObjectId(trip_id))
        if remove_trip is None:
            response = jsonify(data=[])
            response.status_code = 404
            return response


# class Users(Resource):
#     def post(self):
#         new_user = request.json
#         user_collection = app.db.users
#         result = user_collection.insert_one(new_user)
#         my_user = user_collection.find_one({'_user': ObjectId(result.insert_id)})
#         return my_user
#
#     def get(self, user_id):
#         user_collection = app.db.users
#         my_user = user_collection.find_one({'_user': ObjectID(user_id)})
#         if my_user is None:
#             response = jsonify(data=[])
#             response.status_code = 404
#             return response
#         else:
#             user_trips = trip_collection.find()
#             return user_trips

api.add_resource(Trips, '/trips', '/trips/<string: trip_id>')
# api.add_resource(Users, '/users', '/users/<string: user_id>')


@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(JSONEncoder().encode(data), code)
    resp.headers.extend(headers or {})


if __name__ == '__main__':
    app.config['TRAP_BAD_REQUEST_ERRORS'] = True
    app.run(deubg=True)
