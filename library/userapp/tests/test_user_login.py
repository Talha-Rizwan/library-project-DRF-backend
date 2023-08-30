'''Test user login functionality.'''
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from userapp.tests.factories import UserFactory
from userapp.tests.constants import USER_PASSWORD

class UserLoginProfileViewTest(APITestCase):
    '''Class to test all the user login functionality'''
    def setUp(self):
        self.url = reverse('login')
        self.user = UserFactory()


    def test_login_user(self):
        '''Test to login a user using the correct credentials.'''
        data = {
            "username": self.user.username,
            "password": USER_PASSWORD
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['token'])

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
            "password": USER_PASSWORD
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.data['message'], "imvalid credentials")
        self.assertEqual(response.data['data'], {})
