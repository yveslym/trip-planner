from flask import Flask, request, make_response
from flask_restful import Resource, Api
from pymongo import MongoClient
from utils.mongo_json_encoder import JSONEncoder
from bson.objectid import ObjectId
import bcrypt
from mongoengine import *
import pdb
import uuid

app = Flask(__name__)
mongo = MongoClient('localhost', 27017)
app.db = mongo.trip_planner_test
app.bcrypt_rounds = 12
api = Api(app)


## Write Resources here




class Trip(Resource):
    def __init__(self):
        self.name = ''
        self.destination = ''
        self.stop_point = []
        self.completed = False
        self.start_date = ''
        self.user_id = ''
        self.trip_id = uuid.uuid4().hex[:20]

    def post(self):
        trip_collect = app.db.posts
        trip_json = request.json

        name = request.json.get('name')
        destination = request.json.get('destination')
        user = request.json.get('user_id')

        if name is None or destination is None or user is None:
            return({'error':'trip name, destination, and user id are required to create a post'},400,None)
        else:
            app.db.trips.insert_one(trip_json)
            return (trip_json,200,None)

    def get(self):

        #get trip with user id

        user_id = request.args.get('user_id')

        if user_id is not None:
            trip_dict = app.db.trips.find({'user_id':user_id})
            #pdb.set_trace()
            arr = []
            for trip in trip_dict:
                arr.append(trip)
            #pdb.set_trace()
            if arr == []:

                return({'error':' No trip found on the user id argument given'},400,None)
            else:
                return(arr,200,None)

        else:
            return({'error':' no argument passed'},400,None)

    def delete(self):

        #delete single trip with user_id
        if request.args.get('user_id') is not None:
            app.db.posts.delete_one({'user_id':request.args.get('user_id')})
            return ({'delete':'the trip as been deleted'}, 200, None)

        #delete single trip with trip id
        elif request.args.get('_id') is not None:
            app.db.posts.delete_one({'user_id':request.args.get('_id')})
            return ({'delete':'Trip  as been deleted'}, 200, None)


class User(Resource):
    def __init__(self):
        self.first_name = ''  # StringField(required=True, max_length=30)
        self.last_name = ''  # StringField(required=True, max_length=30)
        self.email = ''  # EmailField(required=True, unique=True)
        self.password = '' # StringField (required=True, max_length=30)
        self.username = ''  # StringField(max_length=30)
        self.country = ''

    def post(self):
        user_json = request.json
        user_collect = app.db.users


        user_email = request.json.get('email')
        password = request.json.get('password')

        #pdb.set_trace()

        if 'first_name' in user_json and 'last_name' in user_json and 'email' in user_json:

            # encrypt the password
            encoded_password = password.encode('utf-8')
            hashed = bcrypt.hashpw(encoded_password, bcrypt.gensalt(rounds=12))
            user_json['password'] = str(hashed)
            if self.is_user_exist(user_email) is False:
                user_collect = app.db.users
                user_collect.insert_one(user_json)
                return (user_json, 201, None)
            else:
                return ({'error': 'user exist already'}, 400, None)

        elif 'email' in user_json is None:
            return ({'error': 'no email provided'}, 400, None)
        # elif 'password' in user_json is None:
        #     return ({'error': 'Not password provided'}, 400, None)
        elif 'first_name' in user_json is None or 'last_name' in user_json is None:
            return ({'error': 'either first name or last name were not passed'}, 400, None)
        # else:
        #     return ({'error': 'there is other error'}, 400, None)

    def get(self):


        user_email = request.args.get('email')

        user_country = request.args.get('country')

        if user_country is not None:
            user_dict = app.db.users.find({'country':user_country})
        if user_dict is None:
            return ({'error': 'user does not exist'}, 404, None)
        else:
            arr = []
            for user in user_dict:
                arr.append(user)

            return (arr, 200, None)

    def delete(self):
        email_json = request.args.get('email')

        if self.is_user_exist(email_json) is True:
            user_dict = app.db.users.find_one({'email':email_json})
            app.db.users.remove(user_dict)
            return ({'delete':'the user '+ email_json+ ' as been deleted'}, 200, None)
        else:


            return ({'error': 'User with email ' + email_json + " does not exist"}, 404, None)

    def patch(self):

        #patching user get only one args, email

        email = request.arg.get('email')
        email_json = request.json.get('email')
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        username = request.json.get('username')
        trips_id = request.json.get('trips_id')
        user_collect = app.db.users

        #update email
        if email is not None:
            if email_json is not None:
                user_collect.update({'email':email_json})
                return(user_collect,200,None)
            #update first name
            elif first_name is not None:
                user_collect.update({'first_name':first_name})
                return(user_collect,200,None)
            #update last name
            elif last_name is not None:
                user_collect.update({'last_name':last_name})
                return(user_collect,200,None)
            #update username
            elif username is not None:
                user_collect.update({'username':username})
                return(user_collect,200,None)
            #update_trip--
            elif trips_id is not None:
                # append a new trip id when new trip create
                app.db.users.update({'email': email_json},
                                    {push:{'trips_id':trips_id}}
                                    )

                return(user_collect,200,None)

        else:
            return ({'error':'there is not'+ email+'stored in the database'},404, None)

    def put(self):

        user_email = request.arg

    def is_user_exist(self, email):
        user_collect = app.db.users
        user_dict = user_collect.find_one({'email': email})

        if user_dict is None:
            return False
        else:

            return True


## Add api routes here

api.add_resource(User, '/users')
api.add_resource(Trip, '/trips')


#  Custom JSON serializer for flask_restful
@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(JSONEncoder().encode(data), code)
    resp.headers.extend(headers or {})
    return resp


if __name__ == '__main__':

    # Turn this on in debug mode to get detailled information about request
    # related exceptions: http://flask.pocoo.org/docs/0.10/config/
    app.config['TRAP_BAD_REQUEST_ERRORS'] = True
    app.run(debug=True)
