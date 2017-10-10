import server
from server import *
import unittest
import json
import bcrypt
import base64
from pymongo import MongoClient
from random import  randint
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
        self.assertEqual(response.status_code,201)
        print("end of the post User")

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
        self.assertEqual(post.status_code, 400)

    def test_get_user(self):
        print('______________________TESTING GET USER__________________')
        response = self.app.get('/users',
                                query_string=dict(country = 'usa')
                                )


        response_json = json.loads(response.data.decode())
        print(response_json)
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

        print('NOW DELTETING A NONE EXISTING USER')

        deleted = self.app.delete('/users',
                                  query_string=dict(email=mail)
                                  )

        self.assertEqual(deleted.status_code, 404)
        self.assertEqual(deleted.data.decode("utf-8"), '{"error": "User with email ' + mail + ' does not exist"}')



if __name__ == '__main__':
    unittest.main()
    tripTest = TripPlannerTestCase
    #tripTest.testCreateUser()
