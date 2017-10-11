import server
from server import *
import unittest
import json
import bcrypt
import base64
from pymongo import MongoClient
from random import  randint
from randomUser import Create_user
from randomUser import create_trip
import pdb


class TripPlannerTestCase(unittest.TestCase):
    def setUp(self):

      self.app = server.app.test_client()
      # Run app in testing mode to retrieve exceptions and stack traces
      server.app.config['TESTING'] = True

      mongo = MongoClient('localhost', 27017)
      global db

      # Reduce encryption workloads for tests
      server.app.bcrypt_rounds = 4

      db = mongo.trip_planner_test
      server.app.db = db

      # db.drop_collection('users')
      # db.drop_collection('trips')



    def test_post_user(self):
        print('______________________TESTING INSERT USER__________________')
        new_user = Create_user()
        user = new_user.create()

        response = self.app.post('/users',
                                 headers = None,
                                 data = json.dumps(dict(first_name = user.first_name,
                                                        last_name = user.last_name,
                                                        email = user.email,
                                                        password = "",
                                                        country = user.country,
                                                        username = user.username)),
                                 content_type = 'application/json')
        print('post new user response:')
        print(response)
        self.assertEqual(response.status_code,201)


    # def test_post_with_missing_field(self):
    #
    #     # for this test i purposely omit the email field and expect an error
    #
    #     new_user = Create_user()
    #     user = new_user.create()
    #
    #     response = self.app.post('/users',
    #                              headers=None,
    #                              data=json.dumps(dict(first_name=user.first_name,
    #                                                   last_name=user.last_name,
    #                                                   password="",
    #                                                   country=user.country,
    #                                                   username=user.username)),
    #                              content_type='application/json')
    #
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(response.data.decode("utf-8"), '{"error": "missing fields"}')

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
                                data = json.dumps(dict(first_name = user['first_name'],
                                                       last_name = user['last_name'],
                                                       email = user['email'],
                                                       password = "",
                                                       country = user['country'],
                                                       username = user['username'])),
                                content_type = 'application/json')
        print('post with existing user reponse:')
        print(post)
        self.assertEqual(post.status_code, 400)



    def test_get_user(self):
        print('______________________TESTING GET USER__________________')
        response = self.app.get('/users',query_string=dict(country = 'usa'))

        print('get user response:')
        print(response)
        #response_json = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        print('______________________TESTING DELETING EXISTING AND NONE EXISTING__________________')

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

        #delete user on the picked email


        deleted = self.app.delete('/users',query_string = dict(email = mail))

        print ('user to delete:', mail)
        print('delete user response:')
        print(deleted)
        self.assertEqual(deleted.status_code, 200)



        deleted = self.app.delete('/users', query_string=dict(email=mail))

        print('DELTETING A NONE EXISTING USER')
        print ('user to delete:', mail)
        print('delete user response:')
        print(deleted)
        self.assertEqual(deleted.status_code, 404)
        self.assertEqual(deleted.data.decode("utf-8"), '{"error": "User with email ' + mail + ' does not exist"}')


        #----------------------------------------------------------------------------------#

    def test_post_trip_with_user_id(self):

        print('_____________POST TRIP WITH USER ID______________________')
        #randomly get an array of user by country
        index = randint(0, 3)
        arr = ['usa','canada','uk','france']
        countr = arr[index]
        response = self.app.get('/users',query_string=dict(country = countr))
        # create a new trip
        mytrip = create_trip()
        trip = mytrip.create()

        # randomly get a user dict from array
        users_list = json.loads(response.data.decode())# transform data into list
        ind = randint(0,len(users_list) - 1)
        user = users_list[ind]

        #insert

        trip.user_id = user['_id']

        print('user name: '+user['first_name']+' '+user['last_name'])
        print('trip destination: '+ trip.destination)
        print('user id: '+user['_id'])
        post = self.app.post('/trips',
                      headers = None,
                      data = json.dumps(dict(name = trip.name,
                                             destination = trip.destination,
                                             stop_point = trip.stop_point,
                                             start_date = trip.start_date,
                                             completed = trip.completed,
                                             user_id = trip.user_id,
                                             trips_id = trip.trip_id)),
                      content_type = 'application/json')
        print('post trip with user id response:')
        print(post)
        #pdb.set_trace()
        self.assertEqual(post.status_code, 200)

    def test_trip_post_missing_field(self):

        print('______________________TESTING POST TRIP WITH MISSING FIELD__________________')

        mytrip = create_trip()
        trip = mytrip.create()


        post = self.app.post('/trips',
                      headers = None,
                      data = json.dumps(dict(name = trip.name,
                                             stop_point = trip.stop_point,
                                             start_date = trip.start_date,
                                             completed = trip.completed)),
                      content_type = 'application/json')
        print('post request with missing field:')
        print(post)
        self.assertEqual(post.status_code, 400)

    def test_get_trip_with_user_id(self):

        print('______________________TESTING GET TRIP BY USER ID__________________')

        user_id = '59dcff382ef5263329e934e3'

        get = self.app.get('/trips', query_string = dict(user_id = user_id))

        print('get request answer:')
        print(get)

        self.assertEqual(get.status_code,200)

    def test_get_trip_with_wrong_user_id(self):

        print('______________________TESTING GET GET TRIP WITH WRONG ID__________________')

        user_id = '0000000000000000000000000000'
        wrong = self.app.get('/trips', query_string = dict(user_id = user_id))

        print('get request trip with wrong id answer:')
        print(wrong)
        self.assertEqual(wrong.status_code,400)


    # def test_patch_user(self):
    #
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
    #     Users = Create_user()
    #     newu = Users.create()
    #
    #
    #     patch = self.app.patch('/user',headers = None,
    #                            data = json.dumps(dict( first_name = newu.first_name,
    #                                                   last_name = newu.last_name,
    #                                                   email = newu.email)),
    #                            query_string=dict(email = user['email']),
    #                            content_json ='application/json')
    #     self.assertEqual(patch.status_code,200)








if __name__ == '__main__':
    unittest.main()
    tripTest = TripPlannerTestCase
    #tripTest.testCreateUser()
