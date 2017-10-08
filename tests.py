#import server
from server import *
import unittest
import json
import bcrypt
import base64
from pymongo import MongoClient
import random


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

    # creating 5 user everytime we run the test

    x = 0
    while x < 5:
        file = "/Users/yveslym/Desktop/portfolio/CS1/Hangman_Project/hangman_words.txt"
        name_file = "/Users/yveslym/Desktop/portfolio/MOB2/trip-planner/name.txt"
        domain_file = "/Users/yveslym/Desktop/portfolio/MOB2/trip-planner/domain.txt"
        open_name_file = open(name_file).read().split()
        open_domain_file = open(domain_file).read().split()

        fname = open_name_file[random.randint(0,len(open_name_file)-1)]
        lname = open_name_file[random.randint(0,len(open_name_file)-1)]
        domain_name = open_domain_file[random.randint(0,len(open_domain_file)-1)]

        uname = fname+lname
        emails = fname+'.'+lname+domain_name
        pw = fname+lname+x
        user = User(
            first_name = fname,
            last_name = lname,
            email = emails,
            password = pw,
            username = uname
        )
        user.post()




if __name__ == '__main__':
    unittest.main()
