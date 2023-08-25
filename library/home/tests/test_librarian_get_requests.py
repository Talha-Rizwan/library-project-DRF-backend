from django.contrib.auth.models import Permission

from rest_framework import status
from rest_framework.test import APITestCase

from home.tests.factories import UserBookRequestFactory
from userapp.tests.factories import UserFactory
from userapp.utlis import get_jwt_token

class LibrarianListRequestTestCase(APITestCase):

    def setUp(self):
        self.Requests = UserBookRequestFactory.create_batch(10) # To Do use batch size as a constant here
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
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)
    
    def test_get_all_requests_without_authentication(self):
        self.client.credentials()
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_all_requests_with_simple_user(self):
        data = {
            "username": self.customer_user.username,
            "password": 'password123'
        }
        token = get_jwt_token(data)['data']['token']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

