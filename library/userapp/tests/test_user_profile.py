# from django.test import TestCase
from django.contrib.auth.models import Permission

from rest_framework import status
from rest_framework.test import APITestCase

from userapp.tests.factories import UserFactory
from userapp.serializers import UserSerializer
from userapp.utlis import get_jwt_token
from userapp.models import User

class UserProfileViewTest(APITestCase):
    def setUp(self):
        self.url = '/api/user/user-profile/'
        self.user = UserFactory()
        data = {
            "username": self.user.username,
            "password": 'password123'
        }
        token = get_jwt_token(data)['data']['token']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')


    def test_create_user_profile(self):
        serializer = UserSerializer(UserFactory.build())
        response = self.client.post(self.url, data=serializer.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], 'your account is created')

    def test_create_user_profile_without_username(self):
        serializer = UserSerializer(UserFactory.build())
        data =  serializer.data
        del data['username']        
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_update_user_profile(self):
        update_data = {"full_name": "talha rizwan"}
        response = self.client.put(self.url, data=update_data, format='json')
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.full_name, 'talha rizwan')


    def test_anonymous_user_update_profile(self):
        self.client.credentials()
        update_data = {"full_name": "talha rizwan"}
        response = self.client.put(self.url, data=update_data, format='json')
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
