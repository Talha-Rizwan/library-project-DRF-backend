from django.contrib.auth.models import Permission

from rest_framework import status
from rest_framework.test import APITestCase

from home.serializers import RequestSerializer
from home.tests.factories import UserBookRequestFactory, BookFactory
from userapp.tests.factories import UserFactory
from userapp.utlis import get_jwt_token

class LibrarianDetailRequestTestCase(APITestCase):

    def setUp(self):
        self.Requests = UserBookRequestFactory.create_batch(10) # To Do use batch size as a constant here
        self.url = '/api/home/request/'
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

    def test_get_request(self):
        response = self.client.get(f'{self.url}{self.Requests[0].id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['requested_book'], self.Requests[0].requested_book.id)

    def test_get_request_with_wrong_id(self):
        response = self.client.get(f'{self.url}{1000}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Not found.')

    def test_get_request_unauthorized(self):
        self.client.credentials()
        response = self.client.get(f'{self.url}{self.Requests[0].id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_request_simple_user(self):
        data = {
            "username": self.customer_user.username,
            "password": 'password123'
        }
        token = get_jwt_token(data)['data']['token']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.get(f'{self.url}{self.Requests[0].id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_librarian_approve_request(self):
        response = self.client.put(f'{self.url}{self.Requests[0].id}/',data={"status": "A"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'A')

    def test_librarian_unauthorized_approve_request(self):
        self.client.credentials()
        response = self.client.put(f'{self.url}{self.Requests[0].id}/',data={"status": "A"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_librarian_reject_request(self):
        response = self.client.put(f'{self.url}{self.Requests[0].id}/',data={"status": "R"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'R')
    
    def test_librarian_unauthorized_reject_request(self):
        self.client.credentials()
        response = self.client.put(f'{self.url}{self.Requests[0].id}/',data={"status": "R"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_request_with_wrong_input(self):
        response = self.client.put(f'{self.url}{self.Requests[0].id}/',data={"status": "Incorrect"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

