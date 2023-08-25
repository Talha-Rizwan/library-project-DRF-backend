
from rest_framework import status
from rest_framework.test import APITestCase

from home.serializers import RequestSerializer
from home.tests.factories import UserBookRequestFactory, BookFactory
from userapp.tests.factories import UserFactory
from userapp.utlis import get_jwt_token

class UserRequestTestCase(APITestCase):

    def setUp(self):
        self.Requests = UserBookRequestFactory()
        self.customer_user = self.Requests.request_user
        self.Requests.request_user = self.customer_user
        self.url = '/api/home/user-request/'
  
        data = {
            "username": self.customer_user.username,
            "password": 'password123'
        }
        token = get_jwt_token(data)['data']['token']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        
    def test_create_request(self):
        new_book = BookFactory()
        data = {
            "requested_book" : new_book.id
        }

        response = self.client.post(self.url,data=data, format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data['request_user'], self.customer_user.id)
        self.assertEqual(response.data['requested_book'], new_book.id)
        
    def test_create_request_with_unavailable_book(self):
        data = {
            "requested_book" : 10
        }

        response = self.client.post(self.url,data=data, format='json')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
    
    def test_create_request_with_unauthenticated_client(self):
        self.client.credentials()
        new_book = BookFactory()
        data = {
            "requested_book" : new_book.id
        }

        response = self.client.post(self.url,data=data, format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
    

    def test_user_try_to_create_approved_request(self):
        new_book = BookFactory()
        data = {
            "requested_book" : new_book.id,
            "status" : "A"
        }

        response = self.client.post(self.url,data=data, format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], "P")

    def test_get_requests(self):
        response = self.client.get(self.url)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['books']['requested_books'][0], self.Requests.requested_book.name)

    def test_get_unauthorized_requests(self):
        self.client.credentials()
        response = self.client.get(self.url)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
