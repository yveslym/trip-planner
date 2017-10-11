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

#
# class Pre_Trip1(Document):
#     pass
# class Pre_Trip2(Resource):
#     pass
# class A:
#     __metaclass__ = Pre_Trip1
# class B:
#     __metaclass__ = Pre_Trip2
#
# class Pre_Trip3(Pre_Trip1, Pre_Trip2):
#     pass
#
# class Trip(A,B):
#     __metaclass__ = Pre_Trip3
#
#
#     def test(self):
#         print('trip class work')

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

        user_id = request.json.get('user_d')
        completed = request.json.get('completed')
        start_date = request.json.get('start_date')
        user_id = request.json.get('user_id')
        trip_id = request.json.get('trip_id')

        if name is None:
            return({'error':' trip name field is missing'},400,None)
        elif destination is None:
            return({'error':'trip destination field is missing'},400,None)
        # elif user is None:
        #     return({'error':' user trip field is missing'},400,None)
        elif completed is None:
            return({'error':' trip status trip field is missing'},400,None)
        elif start_date is None:
            return({'error':' trip starting date field is missing'},400,None)
        elif trip_id is None:
            return({'error':' trip starting date field is missing'},400,None)

        elif user_id is not None:
            trip_collect.insert_one(trip_json)
            trip_dict = trip_collect.find_one({'user_id':user_id})
            return (trip_dict,200,None)

        else:
            return (trip_json,200,None)


    def get(self):

        #check if there's trip with current user Reference
        if json.args.get('user_id') is not None:
            trip_dict = app.db.find({'user_id':json.args.get('user_id')})
            if trip_dict is not None:
                arr = []
                for trip in trip_dict:
                    arr.append(trip)
                return(arr,200,None)
            else:
                return({'error':' No trip found for the current user'},400,None)

        elif request.args.get('user_id') is not None and request.args.get('name') is not None:
            trip_dict = app.db.find({'user_id':json.args.get('user_id'),
                                    'name':request.args.get('name')})
            if trip_dict is not None:
                arr = []
                for trip in trip_dict:
                    arr.append(trip)
                return(arr,200,None)
            else:
                return({'error':' No trip found the user and trip name argument given'},400,None)
        else:
            return({'error':' No argument have been passed, enter either user reference or user reference and trip name'},400,None)
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
        self.trips_id = []

    def post(self):
        user_json = request.json
        user_collect = app.db.users
        # user_fname = request.json.get('first_name')
        user_email = request.json.get('email')

        print('USER EMAIL ',user_email )
        if 'first_name' in user_json and 'last_name' in user_json and 'email' in user_json:
            print('json user: ')
            print(user_json)
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
        print(user_email)

        #get user with email
        if user_email is not None:

            user_collect = app.db.users

            user_dict = user_collect.find_one({'email': user_email})

            if user_dict is None:
                return ({'error': 'user '+ user_email+' does not exist'}, 404, None)
            else:
                return (user_dict, 200, None)

        #get multiple user by country

        if user_country is not None:

            user_dict = app.db.users.find({'country':user_country})
            if user_dict is None:
                return ({'error': 'there is not user in this country'}, 404, None)
        else:
            arr = []
            for user in user_dict:
                arr.append(user)
            return (arr, 200, None)

    def delete(self):

        #delete user with all created trips
        email_json = request.args.get('email')
        if self.is_user_exist(email_json) is True:

            #get the user dictionary
            user_dict = app.db.users.find_one({'email':email_json})

            #check if user own trips and delete them
            user_trip = app.db.trips.find({'user_id':user_dict['_id']})
            if user_trip is not None:
                app.db.trips.delte({'user_id':user_dict['_id']})

            #delete user and return appropiete message
            app.db.users.delete({'email':email_json})
            return ({'delete':' user deleted and all posts if he had one or multiple'},200,None)

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
api.add_resource(Trip,'/trips')


#  Custom JSON serializer for flask_restful
@api.representation('application/json')
def output_json(data, code, headers = None):
    resp = make_response(JSONEncoder().encode(data), code)
    resp.headers.extend(headers or {})
    return resp


if __name__ == '__main__':

    # Turn this on in debug mode to get detailled information about request
    # related exceptions: http://flask.pocoo.org/docs/0.10/config/
    app.config['TRAP_BAD_REQUEST_ERRORS'] = True
    app.run(debug=True)
