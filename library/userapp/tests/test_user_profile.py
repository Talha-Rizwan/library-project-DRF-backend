'''Tests to manpulate user profile/account.'''
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from userapp.tests.factories import UserFactory
from userapp.serializers import UserSerializer
from userapp.utlis import get_jwt_token
from userapp.tests.constants import USER_PASSWORD

class UserProfileViewTest(APITestCase):
    '''Class to test the signup and update profile scenarios.'''
    def setUp(self):
        '''
        Setting the url for the api.
        creating a user instance using UserFactory class.
        getting the jwt token for making authenticated requests.
        '''
        self.url = reverse('user_profile')
        self.user = UserFactory()
        data = {
            "username": self.user.username,
            "password": USER_PASSWORD
        }
        token = get_jwt_token(data)['token']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_create_user_profile(self):
        '''Test to create a user without logged in.'''
        serializer = UserSerializer(UserFactory.build())
        response = self.client.post(self.url, data=serializer.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], 'your account is created')

    def test_create_user_profile_without_username(self):
        '''Test to create a user profile without username(required).'''
        serializer = UserSerializer(UserFactory.build())
        data =  serializer.data
        del data['username']
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user_profile(self):
        '''Test to update user profile by sending an authenticated request.'''
        update_data = {"full_name": "talha rizwan"}
        response = self.client.put(self.url, data=update_data, format='json')
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.full_name, 'talha rizwan')
