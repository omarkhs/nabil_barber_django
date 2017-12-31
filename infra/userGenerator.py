from faker import Faker
fake = Faker()

class UserGenerator():
    def __init__( self ):
        self.data = {}

    def generator( self ):
        self.data['username'] = fake.user_name()
        self.data['first_name'] = fake.first_name()
        self.data['last_name'] = fake.last_name()
        self.data['email'] = fake.email()
        self.data['password'] = fake.password()

        phone_number = '+1604'
        for i in range(3):
            #NOTE: middle number cannot be 0 or 1 (check NANP)
            phone_number += str( fake.random_int(min=2,max=9) )
        for i in range(4):
            phone_number += str( fake.random_int(min=0,max=9) )

        self.data['profile'] = { 'phone_number': phone_number }

        return self.data

def generateUser():
    user = UserGenerator()
    return user.generator()


if __name__ == '__main__':
    # For testing purposes
    user = UserGenerator()
    print user.generator()
