# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

# Create your tests here.
class UserTestCase(APITestCase):

    def test_get_all_users( self ):
        response = self.client.post('/user')
        data = {'username': 'ahmed', 'password':'somepass', 'email':'ahmed@test.com',
                'profile':{ 'phone_number' : '+16043621800'} }
        response = self.client.post('/user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get('/user/')
        print response.content

