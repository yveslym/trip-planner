from flask import Flask, request, make_response
from flask_restful import Resource, Api
from pymongo import MongoClient
from utils.mongo_json_encoder import JSONEncoder
from bson.objectid import ObjectId
import bcrypt
from mongoengine import *
import pdb

app = Flask(__name__)
mongo = MongoClient('localhost', 27017)
app.db = mongo.trip_planner_test
app.bcrypt_rounds = 12
api = Api(app)


## Write Resources here


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
    def __init__(self,name,destination):
        self.name = name
        self.destination = destination
        self.stop_point = ListField()
        self.completed = False
        self.start_date = StringField(max_length=20)
        self.user = ReferenceField(User)

    def post(self):
        trip_collect = app.db.posts
        trip_json = request.json


        name = request.json('name')
        destination = request.json('destination')
        user = request.jason('user')

        if name is None or destination is None or user is None:
            return({'error':'both name and destion are required to create a post'},400,None)
        else:
            self.name = name
            self.destination = destination
            self.user = user
            self.completed = False

        if trip_json['stop_point'] is not None:
            self.stop_point = trip_json('stop_point')

        if trip_json['start_date'] is not None:
            self.start_date = trip_json['start_date']

        trip_dict = {self.name,
                     self.destination,
                     self.user,
                     self.stop_point,
                     self.completed,
                     self.start_date}
        trip_collect.insert_one(trip_dict)
        return (trip_dict,200,None)






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
        # user_fname = request.json.get('first_name')

        if 'first_name' in user_json and 'last_name' in user_json and 'email' in user_json:
            print('json user: ')
            print(user_json)
            user_collect = app.db.users
            user_collect.insert_one(user_json)
            return (user_json, 201, None)
        elif 'email' in user_json is None:
            return ({'error': 'no email provided'}, 400, None)
        # elif 'password' in user_json is None:
        #     return ({'error': 'Not password provided'}, 400, None)
        elif 'first_name' in user_json is None or 'last_name' in user_json is None:
            return ({'error': 'either first name or last name were not passed'}, 400, None)
        else:
            return ({'error': 'there is other error'}, 400, None)

    def get(self):

        # user_email = request.args.get('email')
        user_country = request.args.get('country')
        # print(user_email)
        # if user_email is None:
        #     return ({'error': 'no email argument was passed'}, 404, None)
        #
        # user_collect = app.db.users
        #
        # user_dict = user_collect.find_one({'email': user_email})
        # print(user_dict)
        # if user_dict is None:
        #     return ({'error': 'user does not exist'}, 404, None)
        # else:
        #     # arr = []
        #     # for user in user_dict:
        #     #     arr.append(user)
        #
        #     return (user_dict, 200, None)

        #country argument get multy user.

        if user_country is None:
            return ({'error': 'no country argument was passed'}, 404, None)
        user_dict = app.db.users.find({'country':user_country})
        if user_dict is None:
            return ({'error': 'user does not exist'}, 404, None)
        else:
            arr = []
            for user in user_dict:
                arr.append(user)

            return (arr, 200, None)

    def patch(self):
        user_email = request.arg.get('email')
        user_json = request.json
        if user_email is None:
            return ({'error': 'user not found'}, 404, None)

        user_collect = app.db.users
        user_dict = user_collect.find_one({'email': user_email})

        if 'first_name' in user_json is not None:
            user_dict['first_name'] = user_json['first_name']
        elif user_json['email'] is not None:
            user_dict['email'] = user_json['email']
        elif user_json['last_name'] is not None:
            user_dict['last_name'] = user_json['last_name']
        elif user_json['user_name'] is not None:
            user_dict['username'] = user_json['username']
        elif user_json['password'] is not None:
            user_dict['password'] = user_json['password']
        else:
            return ({'error': 'no argument was passed to be save'}, 404, None)

        user_collect.save(user_dict)
        return (user_dict, 200, None)

    def put(self):

        user_email = request.arg

    def is_user_exist(self, email):
        user_collect = app.db.users
        user_dict = user_collect.find_one({'email': email})

        if user_dict is None:

            user_dict = {'first_name': self.first_name,
                         'last_name': self.last_name,
                         'email': self.email,
                         'password': self.password,
                         'username': self.username,
                         'country': self.country}
            user_collect.insert_one(user_dict)

            return False
        else:
            return True


## Add api routes here

api.add_resource(User, '/users')


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
