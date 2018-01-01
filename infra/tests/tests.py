# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import status
from django.contrib.auth.models import User
from userGenerator import generateUser
from testUtils import InfraTestBase

class UserDeleteTestCase(InfraTestBase):

    def setUp( self ):
        self.userInfo = generateUser()
        self.registerUser( self.userInfo )
        self.loginUser( self.userInfo )

    def test_delete_user( self ):
        response = self.client.delete('/user/1/', {}, format='json')
        self.assertEqual( response.status_code, status.HTTP_204_NO_CONTENT)

        all_users = User.objects.all()
        self.assertEqual( len( all_users ), 0 )

    def test_delete_non_existence_user( self ):
        response = self.client.delete('/user/15/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class UserUpdateTestCase(InfraTestBase):

    @classmethod
    def setUpTestData( cls ):
        cls.userInfo = generateUser()

    def prepare( self ):
        self.registerUser( self.userInfo )
        self.loginUser( self.userInfo )

    def update_first_name_case(self):
        data = { 'first_name' : 'omar' }
        response = self.client.patch('/user/1/', data, format='json')

        user = User.objects.get(username=self.userInfo['username'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user.first_name, 'omar')

    def update_last_name_case(self):
        data = { 'last_name' : 'ahmed'}
        response = self.client.patch('/user/1/', data, format='json')

        user = User.objects.get(username=self.userInfo['username'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user.last_name, 'ahmed')

    def update_email_case(self):
        data = { 'email' : 'newEmail@email.com'}
        response = self.client.patch('/user/1/', data, format='json')

        user = User.objects.get(username=self.userInfo['username'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user.email, 'newEmail@email.com')

    def update_password_case(self):
        data = { 'username' : self.userInfo['username'], 'password' : 'newPassword' }
        response = self.client.patch('/user/1/', data, format='json')

        user = User.objects.get(username=self.userInfo['username'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(user.password, 'newPassword')

        # TODO: logout here then re login to verify
        self.loginUser( data )

    def update_profile_case(self):
        data = { 'profile' : { 'phone_number' : '+17789290706' } }
        response = self.client.patch('/user/1/', data, format='json')

        user = User.objects.get(username=self.userInfo['username'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user.profile.phone_number, '+17789290706')

    # This is a test case where unlogged user tries to update any user,
    # You should log out first, then try to update and it should fail
    def update_by_non_logged_user( self ):
        response = self.client.post(self.urls['logout'])
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        data = {}
        data['first_name'] = 'omar'
        response = self.client.patch('/user/1/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def update_by_another_user( self ):
        other_userInfo = generateUser()

        self.registerUser( other_userInfo )
        self.loginUser( other_userInfo )

        # At this point this user has id number 2
        other_user = User.objects.get( username=other_userInfo['username'] )
        self.assertEqual( other_user.id, 2 )

        # Try to change the password of another user
        data = {}
        data['password'] = 'newPasswordToHack'
        response = self.client.patch('/user/1/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        user = User.objects.get(username=self.userInfo['username'])
        #TODO: logout then login with the actual user then try to update


    def test_update( self ):
        self.prepare()

        self.update_first_name_case()
        self.update_last_name_case()
        self.update_email_case()
        self.update_password_case()
        self.update_profile_case()
        self.update_by_non_logged_user()
        self.update_by_another_user()


class UserAdminTestCase(InfraTestBase):
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
        self.loginUser( self.superAdminInfo )

    def barberLogin( self ):
        self.loginUser( self.barberInfo )

    def userLogin( self ):
        self.loginUser( self.userInfo )

    def prepare( self ):
        self.registerUser( self.superAdminInfo )
        self.registerUser( self.barberInfo )
        self.registerUser( self.userInfo )

        pass
        #TODO: to be continued :)

