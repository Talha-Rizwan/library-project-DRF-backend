'''Test user login functionality.'''
from rest_framework import status
from rest_framework.test import APITestCase

from userapp.tests.factories import UserFactory

class UserLoginProfileViewTest(APITestCase):
    '''Class to test all the user login functionality'''
    def setUp(self):
        self.url = '/api/user/login/'
        self.user = UserFactory()
       

    def test_login_user(self):
        '''Test to login a user using the correct credentials.'''
        data = {
            "username": self.user.username,
            "password": 'password123'
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['data']['token'])

    def test_user_invalid_password_login(self):
        '''Test to login a user with invalid password'''
        data = {
            "username": self.user.username,
            "password": 'incorrect'
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.data['message'], "imvalid credentials")
        self.assertEqual(response.data['data'], {})

    def test_user_invalid_username_login(self):
        '''Test to login a user with invalid username.'''
        data = {
            "username": "incorrect",
            "password": 'password123'
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.data['message'], "imvalid credentials")
        self.assertEqual(response.data['data'], {})
