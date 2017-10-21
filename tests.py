import app
from app import *
import unittest
import json
import bcrypt
import base64
from pymongo import MongoClient
from random import  randint
from randomUser import Create_user
from randomUser import create_trip
import pdb
from basicauth import encode
# to use basicauth you need to install the package pip3 install basicauth


def generateBasicAuthHeader(username, password):
    # pdb.set_trace()
    loginString = ("%@:%@"+ username+ password)
    #concatString = username + ":" + password
    utf8 = loginString.encode('utf-8')
    base64String =  base64.b64encode(utf8)
    finalString = "Basic " + str(base64String)

    encoded_str = encode(username,password)
    #username, password = decode(encoded_str)
    return encoded_str


class TripPlannerTestCase(unittest.TestCase):



    def setUp(self):

      self.app = app.app.test_client()
      # Run app in testing mode to retrieve exceptions and stack traces
      app.app.config['TESTING'] = True

      mongo = MongoClient('localhost', 27017)
      global db

      # Reduce encryption workloads for tests
      app.app.bcrypt_rounds = 4

      db = mongo.trip_planner_test
      app.app.db = db

      # db.drop_collection('users')
      # db.drop_collection('trips')



    def test_post_user(self):
        print('______________________TESTING INSERT USER__________________')
        new_user = Create_user()
        user = new_user.create()
        #pdb.set_trace()

        response = self.app.post('/users',
                                 headers = None,
                                 data = json.dumps(dict(first_name = user.first_name,
                                                        last_name = user.last_name,
                                                        email = user.email,
                                                        password = user.password,
                                                        country = user.country,
                                                        username = user.username)),
                                 content_type = 'application/json')
        print('post new user response:')
        print(response)
        self.assertEqual(response.status_code,201)


    def test_post_with_missing_field(self):

        # for this test i purposely omit the email field and expect an error

        new_user = Create_user()
        user = new_user.create()

        response = self.app.post('/users',
                                 headers=None,
                                 data=json.dumps(dict(first_name=user.first_name,
                                                      last_name=user.last_name,
                                                      password="",
                                                      country=user.country,
                                                      username=user.username)),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 400)
        # self.assertEqual(response.data.decode("utf-8"), '{"error": "missing fields"}')

    def test_post_existing_user(self):

        #expect to get an error, with message user exist
        print('______________________TESTING POST EXISTING USER__________________')

        #randomly get a country
        index = randint(0, 3)
        arr = ['usa','canada','uk','france']
        countr = arr[index]

        #randomly get a user from the picked country
        response = self.app.get('/users',
                                query_string=dict(country=countr))
        response_json = json.loads(response.data.decode())

        user_array = []
        for user in response_json:
            user_array.append(user)

        user = user_array[randint(0,len(user_array) -1 )]
        mail = user['email']


        post = self.app.post('/users',
                                headers = None,
                                data = json.dumps(dict(first_name = 'Jacquelyn',
                                                       last_name = 'Rivera',
                                                       email = 'Jacquelyn.Rivera@yahoo.com',
                                                       password = '123456',
                                                       country = 'usa',
                                                       username = 'JacquelynRivera')),
                                content_type = 'application/json')
        print('post with existing user reponse:')
        print(post)
        self.assertEqual(post.status_code, 400)



    def test_get_user(self):
        print('______________________TESTING GET USER__________________')
        response = self.app.get(
            '/users',
            query_string=dict(country = 'usa')
            #headers=dict(generateAuthHeader("some@email.com", "password"))
            )

        print('get user response:')
        print(response)
        #response_json = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)


    def test_delete_user(self):
        print('______________________TESTING DELETING EXISTING AND NONE EXISTING__________________')

        #randomly get a country
        new_user = Create_user()
        user = new_user.create()
        #pdb.set_trace()

        response = self.app.post('/users',
                                 headers = None,
                                 data = json.dumps(dict(first_name = user.first_name,
                                                        last_name = user.last_name,
                                                        email = user.email,
                                                        password = user.password,
                                                        country = user.country,
                                                        username = user.username)),
                                 content_type = 'application/json')
        header_code = generateBasicAuthHeader(user.email,user.password)

        #delete user on the picked email

        deleted = self.app.delete('/users',
                                  headers = dict(authorization=header_code))
                                #   query_string = dict(email = mail))

        print ('user to delete:', user.email)
        print('delete user response:')
        print(deleted)
        self.assertEqual(deleted.status_code, 200)



        deleted = self.app.delete('/users',
                                  headers = dict(authorization=header_code))

        print('DELTETING A NONE EXISTING USER')
        print ('user to delete:', user.email)
        print('delete user response:')
        print(deleted)
        self.assertEqual(deleted.status_code, 400)
        #self.assertEqual(deleted.data.decode("utf-8"), '{"error": "User with email ' + mail + ' does not exist"}')


        #----------------------------------------------------------------------------------#

    # def test_post_trip_with_user_id(self):
    #
    #     print('_____________POST TRIP WITH USER ID______________________')
    #     #randomly get an array of user by country
    #     index = randint(0, 3)
    #     arr = ['usa','canada','uk','france']
    #     countr = arr[index]
    #     response = self.app.get('/users',query_string=dict(country = countr))
    #     # create a new trip
    #     mytrip = create_trip()
    #     trip = mytrip.create()
    #
    #     # randomly get a user dict from array
    #     users_list = json.loads(response.data.decode())# transform data into list
    #     ind = randint(0,len(users_list) - 1)
    #     user = users_list[ind]
    #
    #     #insert
    #
    #     trip.user_id = user['_id']
    #
    #     print('user name: '+user['first_name']+' '+user['last_name'])
    #     print('trip destination: '+ trip.destination)
    #     print('user id: '+user['_id'])
    #     post = self.app.post('/trips',
    #                   headers = None,
    #                   data = json.dumps(dict(name = trip.name,
    #                                          destination = trip.destination,
    #                                          stop_point = trip.stop_point,
    #                                          start_date = trip.start_date,
    #                                          completed = trip.completed,
    #                                          user_id = trip.user_id,
    #                                          trips_id = trip.trip_id)),
    #                   content_type = 'application/json')
    #     print('post trip with user id response:')
    #     print(post)
    #     #pdb.set_trace()
    #     self.assertEqual(post.status_code, 200)
    #
    # def test_trip_post_missing_field(self):
    #
    #     print('______________________TESTING POST TRIP WITH MISSING FIELD__________________')
    #
    #     mytrip = create_trip()
    #     trip = mytrip.create()
    #
    #
    #     post = self.app.post('/trips',
    #                   headers = None,
    #                   data = json.dumps(dict(name = trip.name,
    #                                          stop_point = trip.stop_point,
    #                                          start_date = trip.start_date,
    #                                          completed = trip.completed)),
    #                   content_type = 'application/json')
    #     print('post request with missing field:')
    #     print(post)
    #     self.assertEqual(post.status_code, 400)
    #
    # def test_get_trip_with_user_id(self):
    #
    #     print('______________________TESTING GET TRIP BY USER ID AND GET WRONG USER ID__________________')
    #
    #     user_id = '59dcff382ef5263329e934e3'
    #
    #     get = self.app.get('/trips', query_string = dict(user_id = user_id))
    #
    #     print('get request answer:')
    #     print(get)
    #
    #     self.assertEqual(get.status_code,200)
    #
    #     user_id = '59dcff382ef52633'
    #
    #     get = self.app.get('/trips', query_string = dict(user_id = user_id))
    #
    #     print('get request trip with wrong id answer:')
    #     print(get)
    #
    # def test_get_user_with_email_password(self):
    #     print('______________________TESTING GET USER WITH EMAIL AND PASSWORD AUTH__________________')
    #     get_user = self.app.get('/users',query_string = dict(email = 'Powell.Maximo@yahoo.com',
    #                                                          password = '123456'))
    #     print ('get user with email and password response:')
    #     print (get_user)
    #     self.assertEqual(get_user.status_code,200)
    #
    #


if __name__ == '__main__':
    unittest.main()
    tripTest = TripPlannerTestCase
    #tripTest.testCreateUser()
