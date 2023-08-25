from django.contrib.auth.models import Permission

from rest_framework import status
from rest_framework.test import APITestCase

from userapp.tests.factories import UserFactory
from userapp.serializers import UserSerializer
from userapp.utlis import get_jwt_token
from userapp.models import User

class UserLoginProfileViewTest(APITestCase):
    def setUp(self):
        self.url = '/api/user/login/'
        self.user = UserFactory()
       

    def test_login_user(self):
        data = {
            "username": self.user.username,
            "password": 'password123'
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['data']['token'])

    def test_user_invalid_password_login(self):
        data = {
            "username": self.user.username,
            "password": 'incorrect'
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.data['message'], "imvalid credentials")
        self.assertEqual(response.data['data'], {})

    def test_user_invalid_username_login(self):
        data = {
            "username": "incorrect",
            "password": 'password123'
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.data['message'], "imvalid credentials")
        self.assertEqual(response.data['data'], {})