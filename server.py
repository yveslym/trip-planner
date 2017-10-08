import emails as emails
from flask import Flask, request, make_response
from flask_restful import Resource, Api
from pymongo import MongoClient
from utils.mongo_json_encoder import JSONEncoder
from bson.objectid import ObjectId
import bcrypt
from mongoengine import *


app = Flask(__name__)
mongo = MongoClient('localhost', 27017)
app.db = mongo.trip_planner_development
app.bcrypt_rounds = 12
api = Api(app)


## Write Resources here

class User(Resource, Document):

    first_name = StringField(required=True, max_length=30)
    last_name = StringField(required=True, max_length=30)
    email = EmailField(required=True, unique=True)
    password = StringField (required=True, max_length=30)
    username = StringField(max_length=30)


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
        user_email = request.args.get('email')

        if user_email is None:
            return ({'error':' /(emails) was not  found in the database'}, 404,None)
        user_colect = app.db.users
        user_dict = user_colect.find_one({'email':user_email})

        if user_dict is None:
            return ({'error':'user does not exist'}, 404, None)
        else:
            return (user_dict,200, None)





## Add api routes here

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
