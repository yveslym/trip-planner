
import random
import string

class create_user(Object):
    @staticmethod
    def password(size=8, chars=string.ascii_lowercase+string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def new_user(self):
        file = "/Users/yveslym/Desktop/portfolio/CS1/Hangman_Project/hangman_words.txt"
        name_file = "/Users/yveslym/Desktop/portfolio/MOB2/trip-planner/name.txt"
        domain_file = "/Users/yveslym/Desktop/portfolio/MOB2/trip-planner/domain.txt"
        open_name_file = open(name_file).read().split()
        open_domain_file = open(domain_file).read().split()

        fname = open_name_file[random.randint(0, len(open_name_file) - 1)]
        lname = open_name_file[random.randint(0, len(open_name_file) - 1)]
        domain_name = open_domain_file[random.randint(0, len(open_domain_file) - 1)]
        pword = password()
        uname = fname + lname
        mail = fname + '.' + lname + '@' + domain_name

        user = {'first_name':fname,
                'last_name':lname,
                'email':email,
                'password':create_user.password(),
                'username':uname}
        return(user)


