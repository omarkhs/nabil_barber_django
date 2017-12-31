# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from django.contrib.auth.models import User

import json

# Create your tests here.
class UserRegistrationTestCase(APITestCase):

    def setUp( self ):
        self.userInfo = {'username': 'jackie', 'first_name':'Jack',
        'last_name':'Bell', 'email':'test@test.com',
                'profile':{ 'phone_number' : '+16473459800'} }

    def test_register_short_password( self ):
        '''
        Password must be less than 8 characters for the test to fail
        '''
        data = self.userInfo
        self.userInfo[ 'password' ] = 'short'
        response = self.client.post('/register/', data, format='json')
        self.assertEqual( response.status_code, status.HTTP_400_BAD_REQUEST )

    def test_register_similar_password( self ):
        '''
        Password must be similar to username or any other attribute for the test to fail
        '''
        data = self.userInfo
        self.userInfo[ 'password' ] = 'jackie2'
        response = self.client.post('/register/', data, format='json')
        self.assertEqual( response.status_code, status.HTTP_400_BAD_REQUEST )

    def test_register_password_all_numbers( self ):
        data = self.userInfo
        self.userInfo[ 'password' ] = '4549841514684'
        response = self.client.post('/register/', data, format='json')
        self.assertEqual( response.status_code, status.HTTP_400_BAD_REQUEST )

    def test_register_password_is_common( self ):
        '''
        Common password are based on this list:
            https://docs.djangoproject.com/en/1.11/topics/auth/passwords/#included-validators
        '''
        data = self.userInfo
        self.userInfo[ 'password' ] = 'trustno1'
        response = self.client.post('/register/', data, format='json')
        self.assertEqual( response.status_code, status.HTTP_400_BAD_REQUEST )

    def test_register_good_password( self ):
        data = self.userInfo
        self.userInfo[ 'password' ] = 'rekkfjoi8973f'
        response = self.client.post('/register/', data, format='json')
        self.assertEqual( response.status_code, status.HTTP_201_CREATED )

        username = self.userInfo['username']
        password = self.userInfo[ 'password' ]
        login_data = { 'username': username, 'password': password }
        response = self.client.post('/login/', login_data, secure=False)
        self.assertEqual( response.status_code, status.HTTP_200_OK )

        response = self.client.get('/user/', data, format='json')
        self.assertEqual( response.status_code, status.HTTP_200_OK )
        json = response.json()
        if 'password' in json[0]:
            assert False, 'password retrieved'




class UserDeleteTestCase(APITestCase):

    def setUp( self ):
        self.userInfo = {'username': 'jackie', 'first_name':'Jack',
        'last_name':'Bell', 'email':'test@test.com',
                'profile':{ 'phone_number' : '+16473459800'} }
        self.userInfo[ 'password' ] = 'rotiIXc78_9' # random password :)

        data = self.userInfo
        response = self.client.post('/register/', data, format='json')
        self.assertEqual( response.status_code, status.HTTP_201_CREATED )

        login_data = { 'username': self.userInfo['username'], 'password':
                self.userInfo['password'] }
        response = self.client.post('/login/', login_data, secure=False)
        self.assertEqual( response.status_code, status.HTTP_200_OK )

    def test_delete_user( self ):
        user = User.objects.get( username = 'jackie' )
        self.assertEqual( user.id, 1 )
        response = self.client.delete('/user/1/', {}, format='json')
        self.assertEqual( response.status_code, status.HTTP_202_ACCEPTED )

        all_users = User.objects.all()
        self.assertEqual( len( all_users ), 0 )

    def test_delete_non_existence_user( self ):
        response = self.client.delete('/user/15/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)


class UserUpdateTestCase(APITestCase):

    @classmethod
    def setUpTestData( cls ):
        cls.userInfo = {'username': 'jackie', 'first_name':'Jack',
        'last_name':'Bell', 'email':'test@test.com',
                'profile':{ 'phone_number' : '+16473459800'} }
        cls.userInfo[ 'password' ] = 'rotiIXc78_9'


    def prepare_test( self ):
        response = self.client.post('/register/', self.userInfo, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        login_data = { 'username': self.userInfo['username'], 'password':
                self.userInfo['password'] }
        response = self.client.post('/login/', login_data, secure=False)
        self.assertEqual( response.status_code, status.HTTP_200_OK )

    def update_first_name_test(self):
        data = {}
        data['first_name'] = 'omar'
        response = self.client.put('/user/1/', data, format='json')

        user = User.objects.get(username='jackie')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(user.first_name, 'omar')

    def update_last_name_test(self):
        data = {}
        data['last_name'] = 'ahmed'
        response = self.client.put('/user/1/', data, format='json')

        user = User.objects.get(username='jackie')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(user.last_name, 'ahmed')

    def update_email_test(self):
        data = {}
        data['email'] = 'newEmail@email.com'
        response = self.client.put('/user/1/', data, format='json')

        user = User.objects.get(username='jackie')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(user.email, 'newEmail@email.com')

    def update_password_test(self):
        data = {}
        data['password'] = 'newPassword'
        response = self.client.put('/user/1/', data, format='json')

        user = User.objects.get(username='jackie')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertNotEqual(user.password, 'newPassword')

        # TODO: logout here then re login to verify
        login_data = { 'username': self.userInfo['username'], 'password':
                data['password'] }
        response = self.client.post('/login/', login_data, secure=False)
        self.assertEqual( response.status_code, status.HTTP_200_OK )

    def update_profile_test(self):
        data = { 'profile' : { 'phone_number' : '+17789290706' } }
        response = self.client.put('/user/1/', data, format='json')
        user = User.objects.get(username='jackie')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(user.profile.phone_number, '+17789290706')

    def test_update( self ):
        self.prepare_test()

        self.update_first_name_test()
        self.update_last_name_test()
        self.update_email_test()
        self.update_password_test()
        self.update_profile_test()


class UserLoginLogout(APITestCase):
    def setUp( self ):
        self.userInfo = {'username': 'jackie', 'first_name':'Jack',
        'last_name':'Bell', 'email':'test@test.com',
                'profile':{ 'phone_number' : '+16473459800'} }
        self.userInfo[ 'password' ] = 'rotiIXc78_9'

        data = self.userInfo
        response = self.client.post('/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        login_data = {'username': self.userInfo['username'], 'password':
            self.userInfo['password']}
        response = self.client.post('/login/', login_data, secure=False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        login_data = {'username': self.userInfo['username'], 'password':
            self.userInfo['password']}
        response = self.client.post('/login/', login_data, secure=False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.post('/logout/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, "You're logged out.")

    def test_logout_when_no_user_was_already_loggedIn(self):
        response = self.client.post('/logout/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_logout_when_called_twice(self):
        login_data = {'username': self.userInfo['username'], 'password':
            self.userInfo['password']}
        response = self.client.post('/login/', login_data, secure=False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # first request to logout
        self.client.post('/logout/')
        # calling logout again after user is already logged out
        response = self.client.post('/logout/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)