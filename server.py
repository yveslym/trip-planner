from flask import Flask, request, make_response
from flask_restful import Resource, Api
from pymongo import MongoClient
from utils.mongo_json_encoder import JSONEncoder
from bson.objectid import ObjectId
import bcrypt
from mongoengine import *
import pdb
import uuid
from socket import *
from basicauth import decode
# from basicauth import decode import the decoder
sock=socket()
sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

app = Flask(__name__)
mongo = MongoClient('localhost', 27017)
app.db = mongo.trip_planner_test
rounds = app.bcrypt_rounds = 12
api = Api(app)


## Write Resources here

def user_auth(func):
    def wrapper(*args,**kwargs):
        #pdb.set_trace()
        auth = request.authorization


        username = auth.username
        password = auth.password

        if username is not None and password is not None:
            user_col = app.db.users
            user = user_col.find_one({'email':username})
            if user is not None:
                encoded_pw = password.encode('utf-8')
                #pdb.set_trace()
                if bcrypt.checkpw(encoded_pw, user['password']):
                    return func (*args,**kwargs)
                else:
                    return ({'error': 'email or password is not correct'}, 401, None)
            else:
                return ({'error': 'could not find user in the database'}, 400, None)
        else:
            return ({'error': 'enter both email and password'}, 400, None)


    return wrapper



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


        user_id = request.args.get('user_id')

        if user_id is not None:
            trip_dict = app.db.trips.find({'user_id':user_id})


            if trip_dict is not None:
                arr = []
                for trip in trip_dict:
                    arr.append(trip)

                return(arr,200,None)
            else:
                return({'error':' No trip found the user and trip name argument given'},400,None)
        #check if there's trip with current user Reference
        # elif request.args.get('user_id') is not None:
        #
        #     trip_dict = app.db.trips
        #
        #     trip_dict.find_one({'user_id':request.args.get('user_id')})
        #
        #     # if trip_dict is not None:
        #     #     arr = []
        #     #     for trip in trip_dict:
        #     #         arr.append(trip)
        #     return(trip_dict,200,None)

        # else:
        #     return({'error':' No trip found for the current user'},400,None)


        # else:
        #     return({'error':' No argument have been passed, enter either user reference or user reference and trip name'},400,None)


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
        user_arg = request.args
        user_collect = app.db.users

        #pdb.set_trace()
        user_email = user_json.get('email')
        password = user_json.get('password')
        first_name = user_json.get('first_name')
        last_name =user_json.get('last_name')


        if user_email is None:
            return ({'error': 'no email provided'}, 400, None)

        elif password is None:
            return ({'error': 'no password provided'}, 400, None)

        elif first_name is None:
            return ({'error': 'no first name provided'}, 400, None)

        elif last_name is None:
            return ({'error': 'no last name provided'}, 400, None)

        elif 'first_name' in user_json and 'last_name' in user_json and 'email' in user_json and password is not None:

            # encrypt the password
            encoded_password = password.encode('utf-8')
            user_json['password'] = bcrypt.hashpw(encoded_password, bcrypt.gensalt(rounds))
            if self.is_user_exist(user_email) is False:
                user_collect = app.db.users
                user_collect.insert_one(user_json)
                user = user_collect.find_one({'email':user_email})
                user.pop('password')
                return (user, 201, None)
            else:
                return ({'error': 'user exist already'}, 400, None)



    @user_auth
    def get(self):

        auth = request.authorization

        if auth.username is not None and auth.password is not None:
            user_col = app.db.users
            user = user_col.find_one({'email':auth.username})
            user.pop('password')
            return (user, 200, None)

        if user_email is not None and user_password is not None:
            user_col = app.db.users
            user = user_col.find_one({'email':user_email})
            if user is not None:
                #check password

                password_encoded = user_password.encode('utf-8')
                if bcrypt.hashpw(password_encoded,user['password']) == user['password']:
                    user['password'] = ''
                    return (user,200,None)
                else:
                    return ({'error': 'email or password is not correct'}, 401, None)
            else:
                return ({'error': 'enter email and password'}, 400, None)

        if user_country is None:
            return ({'error': 'no country argument was passed'}, 404, None)
        user_dict = app.db.users.find({'country':user_country})
        if user_dict is None:
            return ({'error': 'user does not exist'}, 404, None)
        else:
            arr = []
            for user in user_dict:
                user.pop('password')
                arr.append(user)

            return (arr, 200, None)

    @user_auth
    def delete(self):

        # pdb.set_trace()
        auth_code = request.headers['authorization']
        #email_json = auth.username('email')
        email_json, password = decode(auth_code)

        if self.is_user_exist(email_json) is True:
            user_dict = app.db.users.find_one({'email':email_json})
            app.db.users.remove(user_dict)
            return ({'delete':'the user '+ email_json+ ' as been deleted'}, 200, None)
        else:


            return ({'error': 'User with email ' + email_json + " does not exist"}, 404, None)

    # def patch(self):
    #     user_email = request.arg.get('email')
    #     user_json = request.json
    #     if user_email is None:
    #         return ({'error': 'user not found'}, 404, None)
    #
    #     user_collect = app.db.users
    #     user_dict = user_collect.find_one({'email': user_email})
    #
    #     if 'first_name' in user_json is not None:
    #         user_dict['first_name'] = user_json['first_name']
    #     elif user_json['email'] is not None:
    #         user_dict['email'] = user_json['email']
    #     elif user_json['last_name'] is not None:
    #         user_dict['last_name'] = user_json['last_name']
    #     elif user_json['user_name'] is not None:
    #         user_dict['username'] = user_json['username']
    #     elif user_json['password'] is not None:
    #         user_dict['password'] = user_json['password']
    #     else:
    #         return ({'error': 'no argument was passed to be save'}, 404, None)
    #
    #     user_collect.save(user_dict)
    #     return (user_dict, 200, None)

#function to authentificate user email and password

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
    app.run(debug=True, port=8080)
