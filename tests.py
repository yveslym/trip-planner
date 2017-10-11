import server
from server import *
import unittest
import json
from pprint import pprint
import bcrypt
import base64
from pymongo import MongoClient
from random import  randint
from randomUser import create_trip
from randomUser import Create_user


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
        print('______________________TESTING POST USER__________________')
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

        post = self.app.post('/users',
                                 headers = None,
                                 data = json.dumps(dict(
                                     first_name = 'Salma',
                                     last_name = 'Janessa',
                                     email = 'Salma.Janessa@aol.com',
                                     country = 'canada',
                                     username = 'SalmaJanesa'

                                 )),
                                 content_type = 'application/json')
        print('post with existing user reponse:')
        print(post)
        self.assertEqual(post.status_code, 400)

    def test_get_user(self):
        #randomly get a country
        index = randint(0, 3)
        arr = ['usa','canada','uk','france']
        countr = arr[index]
        print('______________________TESTING GET USER__________________')
        response = self.app.get('/users',
                                query_string=dict(country = countr)
                                )

        print('get user response:')
        print(response)
        response_json = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        print('______________________TESTING DELETING USER__________________')

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
        print ('user to delete:', mail)

        deleted = self.app.delete('/users',
                                  query_string = dict(email = mail)
                                  )
        self.assertEqual(deleted.status_code, 200)

        print('delete user response:')
        print(deleted)

        deleted = self.app.delete('/users',
                                  query_string=dict(email=mail)
                                  )

        print('delte non existing user response:')
        print(deleted)
        self.assertEqual(deleted.status_code, 404)
        self.assertEqual(deleted.data.decode("utf-8"), '{"error": "User with email ' + mail + ' does not exist"}')


    def test_delete_user_with_all_rips(self):

        #find trips by user id

        deleted = self.app.delete('/users',
                                  query_string=dict(email=mail)
                                  )
        self.assertEqual(deleted.status_code, 404)
        self.assertEqual(deleted.data.decode("utf-8"), '{"error": "User with email ' + mail + ' does not exist"}')






    def test_post_trip_with_user_id(self):

        print('_____________POST TRIP WITH USER ID______________________')
        #randomly get an array of user by country
        index = randint(0, 3)
        arr = ['usa','canada','uk','france']
        countr = arr[index]
        response = self.app.get('/users',
                                query_string=dict(country = countr)
                                )
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
        self.assertEqual(post.status_code, 200)

    def test_trip_post(self):


        print('______________________TESTING POST TRIP__________________')

        mytrip = create_trip()
        trip = mytrip.create()

        post = self.app.post('/trips',
                      headers = None,
                      data = json.dumps(dict(name = trip.name,
                                             destination = trip.destination,
                                             stop_point = trip.stop_point,
                                             start_date = trip.start_date,
                                             completed = trip.completed)),
                      content_type = 'application/json')

        print('post trip response:')
        print(post)
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


if __name__ == '__main__':
    unittest.main()
    tripTest = TripPlannerTestCase
    #tripTest.testCreateUser()
