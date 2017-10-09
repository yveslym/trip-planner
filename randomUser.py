import server
from server import *
import random
import string

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
        user.password = ''
        user.username = uname


        return(user)
