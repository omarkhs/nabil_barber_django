from userGenerator import generateUser
from testUtils import InfraTestBase
from rest_framework import status
from django.contrib.auth.models import User

class UserRegistrationSimpleTestCase(InfraTestBase):
    @classmethod
    def setUpTestData( cls ):
        cls.userInfo = generateUser()

    # Password must be less than 8 characters for the test to fail
    def test_register_short_password( self ):
        self.userInfo[ 'password' ] = 'short'
        self.registerUser( self.userInfo, fail=True )

    # Password must be similar to username or any other attribute for the test to fail
    def test_register_similar_password( self ):
        self.userInfo[ 'password' ] = 'jackie2'
        self.registerUser( self.userInfo, fail=True )

    def test_register_password_all_numbers( self ):
        self.userInfo[ 'password' ] = '4549841514684'
        self.registerUser( self.userInfo, fail=True )

    # Common password are based on this list:
    # https://docs.djangoproject.com/en/1.11/topics/auth/passwords/#included-validators
    def test_register_password_is_common( self ):
        self.userInfo[ 'password' ] = 'trustno1'
        self.registerUser( self.userInfo, fail=True )

    def test_register_good_password( self ):
        data = self.userInfo
        self.userInfo[ 'password' ] = 'rekkfjoi8973f'
        response = self.registerUser( self.userInfo )
        json = response.json()
        if 'password' in json:
            assert False, 'password retrieved'

        self.loginUser( self.userInfo )


class UserLoginLogoutSimpleTestCase(InfraTestBase):
    @classmethod
    def setUpTestData( cls ):
        cls.userInfo = generateUser()

    def prepare( self ):
        self.registerUser( self.userInfo )

    def init_login(self):
        self.loginUser( self.userInfo )

    def logout(self):
        response = self.client.post(self.urls['logout'])
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def logout_when_no_user_was_already_loggedIn(self):
        response = self.client.post(self.urls['logout'])
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def logout_when_called_twice(self):
        self.loginUser( self.userInfo )

        # first request to logout
        response = self.client.post(self.urls['logout'])
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        # calling logout again after user is already logged out
        response = self.client.post(self.urls['logout'])
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_login_logout_simple_test(self):
        self.prepare()
        self.init_login()
        self.logout()
        self.logout_when_no_user_was_already_loggedIn()
        self.logout_when_called_twice()
