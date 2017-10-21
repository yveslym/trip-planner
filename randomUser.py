import app
from app import Trip
from app import User
import random
from random import randint
import string
import datetime

class Create_user(object):

    def password(size=8, chars=string.ascii_lowercase+string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))


    def create(self):
        name_file = "/Users/yveslym/Desktop/portfolio/MOB2/trip-planner/name.txt"
        domain_file = "/Users/yveslym/Desktop/portfolio/MOB2/trip-planner/domain.txt"
        country_file = "/Users/yveslym/Desktop/portfolio/MOB2/trip-planner/country.txt"

        open_country_file = open(country_file).read().split()
        open_name_file = open(name_file).read().split()
        open_domain_file = open(domain_file).read().split()

        country = open_country_file[random.randint(0,len(open_country_file)-1)]
        fname = open_name_file[random.randint(0, len(open_name_file) - 1)]
        lname = open_name_file[random.randint(0, len(open_name_file) - 1)]
        domain_name = open_domain_file[random.randint(0, len(open_domain_file) - 1)]

        uname = fname + lname
        mail = fname + '.' + lname + '@' + domain_name


        user = User()
        user.first_name = fname
        user.last_name = lname
        user.email = mail
        user.country = country
        user.password = '123456'
        user.username = uname
        return(user)

class create_trip(object):
    def create(self):
        trip = Trip()
        coutry_arr = ['france','uk','usa','canada']
        france_arr = ['paris','marseille','bordeaux','nice','lyon','toulouse','lille','monpelier','nante']
        uk_arr = ['london','manchester','leads','liverpool','newcastel','combridge','glasgow','oxford']
        usa_arr = ['san fransico','new york','washington','los angeles','miami','ohio','philladelphia','oakland','new jersey']
        canada_arr = ['toronto','ottawa','Vancouver','Montreal','Calgary','Edmonton','Quebec','victoria','Sakatoon','Kingston','Regina']
        i = 0
        while i < 100:
            dest_index = randint(0,len(coutry_arr)-1)
            i = i+1
        stop_point = []
        destination = coutry_arr[dest_index]
        if destination == 'france':
            i = 0
            while i<5:
                fr_index =  randint(0,len(france_arr)-1)
                stop_point.append(france_arr[fr_index])
                del france_arr[fr_index]
                i = i+1
        elif destination == 'uk':
            i = 0
            while i<5:
                uk_index = randint(0,len(uk_arr)-1)
                stop_point.append(uk_arr[uk_index])
                del uk_arr[uk_index]
                i = i+1
        elif destination == 'usa':
            i = 0
            while i<5:
                usa_index = randint(0,len(usa_arr)-1)
                stop_point.append(usa_arr[usa_index])
                del usa_arr[usa_index]
                i = i+1

        elif destination =='canada':
            i = 0
            while i<5:
                canada_index = randint(0,len(canada_arr)-1)
                stop_point.append(canada_arr[canada_index])
                del canada_arr[canada_index]
                i = i+1

        trip_name = 'my trip to '+destination

        trip = Trip()
        trip.destination = destination
        trip.name = trip_name
        trip.stop_point = stop_point
        trip.start_date = str(datetime.date.today())
        #print(trip.trip_id)
        return trip

            # print (trip.name)
            # print(trip.destination)
            # print(trip.stop_point)
            # print(trip.start_date)
            # print(trip.completed)
# if __name__=='__main__':
#     trip = create_trip()
#     trip.create()
