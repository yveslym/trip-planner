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

class User(Resource):

    first_name = ""#StringField(required=True, max_length=30)
    last_name = ""#StringField(required=True, max_length=30)
    email = ""#EmailField(required=True, unique=True)
    password = ""#StringField (required=True, max_length=30)
    username = ""#StringField(max_length=30)
    country = ""


    def post(self):
        user_dict = request.json
        user_collect = app.db.users

        if 'first_name' in user_dict and 'last_name' in user_dict and 'email' in user_dict and 'pasword' in user_dict:
            post = user_collect.insert_one(user_dict)
            return (post, 201, None)
        elif 'email' in user_dict is None:
            return ({'error':'no email provided'}, 400, None)
        elif 'password' in user_dict is None:
            return ({'error':'Not password provided'}, 400, None)
        elif 'first_name' in user_dict is None or 'last_name' in user_dict is None:
            return ({'error':'either first name or last name were not passed'}, 400, None)
        else:
            return ({'error':'there is other error'},400, None)

    def get(self):

        user_country = request.args.get('country')
        print(user_country)
        if user_country is None:
            print ('country ',user_country)
            return ({'error':'country was not  found in the database'}, 404,None)
        user_collect = app.db.users
        # pdb.set_trace()
        user_dict = user_collect.find({
            'country': 'usa'
        })
        print(user_dict)
        if user_dict is None:
            return ({'error':'user does not exist'}, 404, None)
        else:
            arr = []
            for user in user_dict:
                arr.append(user)
                print(user)
            return (arr,200, None)
        # user_col = app.db.users
        #
        # user = user_col.find_one({
        #     'email': 'Shea.Boone@dawnsonmail.com'
        # })
        #
        # if not user:
        #     return ({'error': 'why the fuck?'}, 404, None)
        # else:
        #     return (user, 200, None)

    def is_user_exist(self, email):
        user_collect = app.db.users
        user_dict = user_collect.find_one({'email': email})

        if user_dict is None:

            user_dict = {'first_name':self.first_name,
                         'last_name':self.last_name,
                         'email': self.email,
                         'password':self.password,
                         'username':self.username,
                         'country':self.country}
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
