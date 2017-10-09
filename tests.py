import server
from server import *
import unittest
import json
import bcrypt
import base64
from pymongo import MongoClient
import random
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

      db.drop_collection('users')
      db.drop_collection('trips')

    # User tests, fill with test methods
    def testCreateUser(self):

    #creating 5 user everytime we run the test
        index = 0
        while index < 10:
            user = Create_user.create()
            index = index+1

    def test_post_user(self):
        user = Create_user.create()
        response = self.app.post('/users',
                                 headers = None,
                                 data = json.dump(dict(user)),
                                 content_type = 'application/json')
        self.assertEqual(response.status_code,201)
        print("end of the post User")

        # response = self.app.post('/users',
        #                          headers=None,
        #                          data=json.dumps(dict(
        #                              username="Eliel Gordon",
        #                              email="eliel@example.com",
        #                              password="password"
        #                          )),
        #                          content_type='application/json')
        #
        # self.assertEqual(response.status_code, 201)



        # print("end of inser user text")




if __name__ == '__main__':
    unittest.main()
    tripTest = TripPlannerTestCase
    tripTest.testCreateUser()
