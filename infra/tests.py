# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from userGenerator import generateUser

REGISTRATION_URL = '/register/'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'


def loginUser( data ):
    login_data = {'username': data['username'], 'password': data['password']}
    response = self.client.post(LOGIN_URL, login_data, secure=False)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

def registerUser( self, data, fail=False ):
    response = self.client.post(REGISTRATION_URL, data, format='json')
    if not fail:
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    else:
        self.assertEqual( response.status_code, status.HTTP_400_BAD_REQUEST )

# Must be inhereited with APITestCase
class TestCaseMixin():
    def loginUser( self, data ):
        login_data = {'username': data['username'], 'password': data['password']}
        response = self.client.post(LOGIN_URL, login_data, secure=False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def registerUser( self, data, fail=False ):
        response = self.client.post(REGISTRATION_URL, data, format='json')
        if not fail:
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        else:
            self.assertEqual( response.status_code, status.HTTP_400_BAD_REQUEST )


# Create your tests here.
class UserRegistrationTestCase(APITestCase, TestCaseMixin):

    def setUp( self ):
        self.userInfo = generateUser()

    def test_register_short_password( self ):
        '''
        Password must be less than 8 characters for the test to fail
        '''
        self.userInfo[ 'password' ] = 'short'
        self.registerUser( self.userInfo, fail=True )

    def test_register_similar_password( self ):
        '''
        Password must be similar to username or any other attribute for the test to fail
        '''
        self.userInfo[ 'password' ] = 'jackie2'
        self.registerUser( self.userInfo, fail=True )

    def test_register_password_all_numbers( self ):
        self.userInfo[ 'password' ] = '4549841514684'
        self.registerUser( self.userInfo, fail=True )

    def test_register_password_is_common( self ):
        '''
        Common password are based on this list:
            https://docs.djangoproject.com/en/1.11/topics/auth/passwords/#included-validators
        '''
        self.userInfo[ 'password' ] = 'trustno1'
        self.registerUser( self.userInfo, fail=True )

    def test_register_good_password( self ):
        data = self.userInfo
        self.userInfo[ 'password' ] = 'rekkfjoi8973f'
        self.registerUser( self.userInfo )

        self.loginUser( self.userInfo )

        response = self.client.get('/user/', data, format='json')
        self.assertEqual( response.status_code, status.HTTP_200_OK )
        json = response.json()
        if 'password' in json[0]:
            assert False, 'password retrieved'


class UserDeleteTestCase(APITestCase, TestCaseMixin):

    def setUp( self ):
        self.userInfo = generateUser()
        self.registerUser( self.userInfo )
        self.loginUser( self.userInfo )

    def test_delete_user( self ):
        response = self.client.delete('/user/1/', {}, format='json')
        self.assertEqual( response.status_code, status.HTTP_202_ACCEPTED )

        all_users = User.objects.all()
        self.assertEqual( len( all_users ), 0 )

    def test_delete_non_existence_user( self ):
        response = self.client.delete('/user/15/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)


class UserUpdateTestCase(APITestCase, TestCaseMixin):

    @classmethod
    def setUpTestData( cls ):
        cls.userInfo = generateUser()

    def prepare( self ):
        self.registerUser( self.userInfo )
        self.loginUser( self.userInfo )

    def update_first_name_case(self):
        data = { 'first_name' : 'omar' }
        response = self.client.put('/user/1/', data, format='json')

        user = User.objects.get(username=self.userInfo['username'])
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(user.first_name, 'omar')

    def update_last_name_case(self):
        data = { 'last_name' : 'ahmed'}
        response = self.client.put('/user/1/', data, format='json')

        user = User.objects.get(username=self.userInfo['username'])
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(user.last_name, 'ahmed')

    def update_email_case(self):
        data = { 'email' : 'newEmail@email.com'}
        response = self.client.put('/user/1/', data, format='json')

        user = User.objects.get(username=self.userInfo['username'])
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(user.email, 'newEmail@email.com')

    def update_password_case(self):
        data = { 'username' : self.userInfo['username'], 'password' : 'newPassword' }
        response = self.client.put('/user/1/', data, format='json')

        user = User.objects.get(username=self.userInfo['username'])
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertNotEqual(user.password, 'newPassword')

        # TODO: logout here then re login to verify
        self.loginUser( data )

    def update_profile_case(self):
        data = { 'profile' : { 'phone_number' : '+17789290706' } }
        response = self.client.put('/user/1/', data, format='json')

        user = User.objects.get(username=self.userInfo['username'])
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(user.profile.phone_number, '+17789290706')

    def test_update( self ):
        self.prepare()

        self.update_first_name_case()
        self.update_last_name_case()
        self.update_email_case()
        self.update_password_case()
        self.update_profile_case()


class UserLoginLogout(APITestCase, TestCaseMixin):
    def setUp( self ):
        self.userInfo = generateUser()
        self.registerUser( self.userInfo )

    def test_login(self):
        self.loginUser( self.userInfo )

    def test_logout(self):
        self.loginUser( self.userInfo )
        response = self.client.post(LOGOUT_URL)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_logout_when_no_user_was_already_loggedIn(self):
        response = self.client.post(LOGOUT_URL)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_logout_when_called_twice(self):
        self.loginUser( self.userInfo )

        # first request to logout
        response = self.client.post(LOGOUT_URL)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        # calling logout again after user is already logged out
        response = self.client.post(LOGOUT_URL)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class UserAdminTestCase(APITestCase):
    @classmethod
    #TODO: Discuss the permissions of Barber against SuperAdmin
    def setUpTestData( cls ):
        '''
        SuperAdmin is the first user created
        Barber is a user that is part of the Barber group and is_staff field is True
        Non-admins are just regular users: customers
        '''

        cls.superAdminInfo = generateUser()

        cls.barberInfo = generateUser()

        cls.userInfo = generateUser()

    def superAdminLogin( self ):
        loginUser( self.superAdminInfo )

    def barberLogin( self ):
        loginUser( self.barberInfo )

    def userLogin( self ):
        loginUser( self.userInfo )

    def prepare( self ):
        registerUser( self.superAdminInfo )
        registerUser( self.barberInfo )
        registerUser( self.userInfo )

        pass
        #TODO: to be continued :)

