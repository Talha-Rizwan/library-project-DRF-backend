'''Tests to close request user book request.'''
from django.contrib.auth.models import Permission

from rest_framework import status
from rest_framework.test import APITestCase

from userapp.tests.factories import UserFactory
from userapp.utlis import get_jwt_token
from home.tests.constants import BATCH_SIZE, FORMAT
from home.tests.factories import UserBookRequestFactory

class LibrarianCloseRequestTestCase(APITestCase):
    '''
    Class to test CloseBookRequest view. 
    The api url /api/home/close-request/
    '''
    def setUp(self):
        '''
        Create multiple user pending request instances.
        creating user to two types i-e simple user and librarain.
        '''
        self.requests = UserBookRequestFactory.create_batch(BATCH_SIZE)
        self.url = '/api/home/close-request/'
        self.customer_user = UserFactory()
        self.librarian_user = UserFactory()
        librarian = Permission.objects.get(codename='is_librarian')
        self.librarian_user.user_permissions.add(librarian)
        self.librarian_user.save()
        self.requests[0].status = 'B'
        self.requests[0].save()

        data = {
            "username": self.librarian_user.username,
            "password": 'password123'
        }
        token = get_jwt_token(data)['data']['token']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_librarian_close_request(self):
        '''Test to close user request with B status by a librarian user.'''
        response = self.client.put(
            f'{self.url}{self.requests[0].id}/',
            data={"status": "C"},
            format=FORMAT
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'C')

    def test_librarian_unauthorized_close_request(self):
        '''Test to close user request with B status by an anonymous user.'''
        self.client.credentials()
        response = self.client.put(
            f'{self.url}{self.requests[0].id}/',
            data={"status": "A"},
            format=FORMAT
            )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_request_with_wrong_input(self):
        '''Test to send wrong body data to api using librarian user.'''
        response = self.client.put(
            f'{self.url}{self.requests[0].id}/',
            data={"status": "Incorrect"},
            format=FORMAT
            )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_librarain_close_non_existant_request(self):
        '''Test to update the status of a request that doesnot exist.'''
        response = self.client.put(
            f'{self.url}100/',
            data={"status": "C"},
            format=FORMAT
            )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_close_request_without_permissions(self):
        '''Test to close a request with a simple unauthorized user.'''
        data = {
            "username": self.customer_user.username,
            "password": 'password123'
        }
        token = get_jwt_token(data)['data']['token']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(
            f'{self.url}{self.requests[0].id}/',
            data={"status": "A"},
            format=FORMAT
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
