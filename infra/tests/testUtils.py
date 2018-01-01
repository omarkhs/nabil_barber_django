from rest_framework.test import APITestCase
from rest_framework import status

class InfraTestBase( APITestCase ):
    def __init__( self, *args, **kwargs ):
        super( APITestCase, self).__init__( *args, **kwargs )
        self.urls = {}
        self.setupUrls()

    def setupUrls( self ):
        self.urls['register'] = '/register/'
        self.urls['login'] = '/login/'
        self.urls['logout'] = '/logout/'

    def loginUser( self, data ):
        login_data = {'username': data['username'], 'password': data['password']}
        response = self.client.post(self.urls['login'], login_data, secure=False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def registerUser( self, data, fail=False ):
        response = self.client.post(self.urls['register'], data, format='json')
        if not fail:
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        else:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        return response

