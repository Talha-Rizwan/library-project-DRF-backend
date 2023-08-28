'''Tests to get all user pending request by librarian user.'''

from django.contrib.auth.models import Permission

from rest_framework import status
from rest_framework.test import APITestCase

from home.tests.factories import UserBookRequestFactory
from home.tests.constants import BATCH_SIZE, FORMAT
from userapp.tests.factories import UserFactory
from userapp.utlis import get_jwt_token

class LibrarianListRequestTestCase(APITestCase):
    '''Class to evaluate all the scenarios of ListBookRequestView'''

    def setUp(self):
        '''
        Create different requests with status pending.
        Creating simple and librarian user.
        Getting the jwt authentication token for librarian user.
        '''
        self.requests = UserBookRequestFactory.create_batch(BATCH_SIZE)
        self.url = '/api/home/all-request/'
        self.customer_user = UserFactory()
        self.librarian_user = UserFactory()
        librarian = Permission.objects.get(codename='is_librarian')
        self.librarian_user.user_permissions.add(librarian)
        self.librarian_user.save()

        data = {
            "username": self.librarian_user.username,
            "password": 'password123'
        }
        token = get_jwt_token(data)['data']['token']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_get_all_requests(self):
        '''Test to get all the pending user requests by librarian user'''
        response = self.client.get(self.url, format=FORMAT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), BATCH_SIZE)

    def test_get_all_requests_without_authentication(self):
        '''Test to get all reqests using anonymous user.'''
        self.client.credentials()
        response = self.client.get(self.url, format=FORMAT)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_all_requests_with_simple_user(self):
        '''Test to get all user requests using simple user account.'''
        data = {
            "username": self.customer_user.username,
            "password": 'password123'
        }
        token = get_jwt_token(data)['data']['token']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(self.url, format=FORMAT)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
