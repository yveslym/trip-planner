import server
from server import *
import unittest
import json
import bcrypt
import base64
from pymongo import MongoClient
import random
from randomUser import Create_user
import string

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
        self.assertEqual(response.data.decode("utf-8"), '{"error": "missing fields"}')







if __name__ == '__main__':
    unittest.main()
    tripTest = TripPlannerTestCase
    #tripTest.testCreateUser()

