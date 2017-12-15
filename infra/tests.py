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
        response = self.client.post('/user/', data, format='json')
        self.assertEqual( response.status_code, status.HTTP_400_BAD_REQUEST )

    def test_register_similar_password( self ):
        '''
        Password must be similar to username or any other attribute for the test to fail
        '''
        data = self.userInfo
        self.userInfo[ 'password' ] = 'jackie2'
        response = self.client.post('/user/', data, format='json')
        self.assertEqual( response.status_code, status.HTTP_400_BAD_REQUEST )

    def test_register_password_all_numbers( self ):
        data = self.userInfo
        self.userInfo[ 'password' ] = '4549841514684'
        response = self.client.post('/user/', data, format='json')
        self.assertEqual( response.status_code, status.HTTP_400_BAD_REQUEST )

    def test_register_password_is_common( self ):
        '''
        Common password are based on this list:
            https://docs.djangoproject.com/en/1.11/topics/auth/passwords/#included-validators
        '''
        data = self.userInfo
        self.userInfo[ 'password' ] = 'trustno1'
        response = self.client.post('/user/', data, format='json')
        self.assertEqual( response.status_code, status.HTTP_400_BAD_REQUEST )


class UserDeleteTestCase(APITestCase):

    def setUp( self ):
        self.userInfo = {'username': 'jackie', 'first_name':'Jack',
        'last_name':'Bell', 'email':'test@test.com',
                'profile':{ 'phone_number' : '+16473459800'} }
        self.userInfo[ 'password' ] = 'rotiIXc78_9' # random password :)

        data = self.userInfo
        response = self.client.post('/user/', data, format='json')
        self.assertEqual( response.status_code, status.HTTP_201_CREATED )

    def test_delete_user( self ):
        user = User.objects.get( username = 'jackie' )
        self.assertEqual( user.id, 1 )
        response = self.client.delete('/user/1/', {}, format='json')
        self.assertEqual( response.status_code, status.HTTP_202_ACCEPTED )

        all_users = User.objects.all()
        self.assertEqual( len( all_users ), 0 )

    def test_delete_non_existence_user( self ):
        response = self.client.delete('/user/15/', {}, format='json')
        self.assertEqual( response.status_code, status.HTTP_406_NOT_ACCEPTABLE )
