from flask import Flask, request, make_response
from flask_restful import Resource, Api
from pymongo import MongoClient
# from bson.objectid import ObjectId
import bcrypt
import json
from CustomClass import JSONEncoder
from flask import jsonify
import pdb
from bson import json_util
# from bson.json_util import dumps
import uuid
# from basicauth import encode, decode

# from basicauth import decode import the decoder
#sock=socket()
#sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

app = Flask(__name__)
mongo = MongoClient('localhost', 27017)
app.config.from_pyfile('config.cfg')
# mongo = MongoClient(app.config['MONGO_CLIENT'])
app.db = mongo.trip_planner_test
rounds = app.bcrypt_rounds = 8
api = Api(app)


## Write Resources here

def user_auth(func):
    def wrapper(*args,**kwargs):
        #pdb.set_trace()
        auth = request.authorization


        username = auth.username
        password = auth.password
        #pdb.set_trace()
        if username is not None and password is not None:
            user_col = app.db.users
            user = user_col.find_one({'email':username})

            if user is not None:
                encoded_pw = password.encode("utf-8")

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
    @user_auth
    def post(self):

        trip_collect = app.db.trips
        trip_json = request.json

        name = request.json.get('name')
        destination = request.json.get('destination')
        user = request.json.get('user_id')

        #pdb.set_trace()
        #print(name+ " "+" "+destination+" "+user)

        if name is None or destination is None or user is None:
            return({'error':'trip name, destination, and user id are required to create a post'},400,None)
        else:
            trip_collect.insert_one(trip_json)
            return (trip_json,200,None)
    @user_auth
    def get(self):

        #pdb.set_trace()
        user_id = request.headers.get('user_id')
        #pdb.set_trace()
        trips_col = app.db.trips
        if user_id is not None:
            trip_dict = trips_col.find({'user_id':user_id})

            if trip_dict is not None:
                arr = []
                for trip in trip_dict:
                    arr.append(trip)
                    json.dumps(arr, default=json_util.default)
                return(arr,200,None)
            else:
                return({'error':' No trip found the user and trip name argument given'},400,None)
    @user_auth
    def delete(self):

        #delete single trip with user_id
        if request.args.get('user_id') is not None:
            app.db.posts.delete_one({'user_id':request.args.get('user_id')})
            return ({'delete':'the trip as been deleted'}, 200, None)

        #delete single trip with trip id
        elif request.args.get('_id') is not None:
            app.db.posts.delete_one({'user_id':request.args.get('_id')})
            return ({'delete':'Trip  as been deleted'}, 200, None)

    @user_auth
    def put(self):

        json_data = request.json

        user_id = json_data.get('user_id')

        trip_col = app.db.trips
        if request.json('destination') is not None:
            dest = json('destination')
            trip_col.find_one_and_update({'_id':user_id},{'destination':dest})
        elif request.json('name') is not None:
            name = request.json('name')
            trip_col.find_one_and_update({'_id': user_id}, {'name': name})
        elif request.json('stop_point') is not None:
            stopP = request.json('stop_point')
            #trip_col.find_one_and_update({'_id':user_id},{$push:{'end_point':stopP}})



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
            # pdb.set_trace()
            hashed = bcrypt.hashpw(encoded_password, bcrypt.gensalt(rounds))
            user_json['password'] = hashed

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
        user_col = app.db.users
        user = user_col.find_one({'email':auth.username})
        user.pop('password')
        return (user, 200, None)


    @user_auth
    def delete(self):

        # pdb.set_trace()
        auth_code = request.headers['authorization']

        auth = request.authorization
        user_dict = app.db.users.find_one({'email':auth.username})
        app.db.users.remove(user_dict)
        return ({'delete':'the user '+ auth.username+ ' as been deleted'}, 200, None)


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
    app.run(debug=True, port=8088)
