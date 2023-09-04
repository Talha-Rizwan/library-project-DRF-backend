'''Test to create/get a user book request.'''
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from home.tests.factories import UserBookRequestFactory, BookFactory
from home.tests.constants import FORMAT, INVALID_ID
from home.constants import APPROVED_STATUS, PENDING_STATUS
from userapp.tests.constants import USER_PASSWORD
from userapp.utlis import get_jwt_token

class UserRequestTestCase(APITestCase):
    '''Class to evaluate all the scenarios of UserBookRequestView.'''
    def setUp(self):
        '''
        Create Request with status pending.
        Creating simple user.
        Getting the jwt authentication token for user.
        '''
        self.request = UserBookRequestFactory()
        self.customer_user = self.request.request_user
        self.request.request_user = self.customer_user
        self.url = reverse('pending_request')

        data = {
            "username": self.customer_user.username,
            "password": USER_PASSWORD
        }
        token = get_jwt_token(data)['token']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')


    def test_create_request(self):
        '''Test to create a user pending book request by a customer user.'''
        new_book = BookFactory()
        data = {
            "requested_book" : new_book.id
        }

        response = self.client.post(self.url,data=data, format=FORMAT)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data['request_user'], self.customer_user.id)
        self.assertEqual(response.data['requested_book'], new_book.id)

    def test_create_request_with_unavailable_book(self):
        '''Test to create a user request for a book that doesnot exist.'''
        data = {
            "requested_book" : INVALID_ID
        }

        response = self.client.post(self.url,data=data, format=FORMAT)
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

    def test_create_request_with_unauthenticated_client(self):
        '''Test to create a user request without authentication.'''
        self.client.credentials()
        new_book = BookFactory()
        data = {
            "requested_book" : new_book.id
        }

        response = self.client.post(self.url,data=data, format=FORMAT)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_user_try_to_create_approved_request(self):
        '''Test to create user request by setting a different status except for pending.'''
        new_book = BookFactory()
        data = {
            "requested_book" : new_book.id,
            'status' : APPROVED_STATUS
        }
        response = self.client.post(self.url,data=data, format=FORMAT)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], PENDING_STATUS)

    def test_get_requests(self):
        '''Test to get all the user request books.'''
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['books']['requested_books'][0],
            self.request.requested_book.name
            )

    def test_get_unauthorized_requests(self):
        '''Test to get all the user request books without authentication.'''
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
