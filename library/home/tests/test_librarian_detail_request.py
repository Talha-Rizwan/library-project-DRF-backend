'''Tests to get or approve/reject user pending request.'''
from django.contrib.auth.models import Permission
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from home.tests.factories import UserBookRequestFactory
from home.tests.constants import BATCH_SIZE, FORMAT
from home.constants import APPROVED_STATUS, REJECTED_STATUS
from userapp.tests.constants import USER_PASSWORD
from userapp.constants import LIBRARIAN_PERMISSION
from userapp.tests.factories import UserFactory
from userapp.utlis import get_jwt_token

class LibrarianDetailRequestTestCase(APITestCase):
    '''Test class to check all the scenarios of DetailBookRequestView'''

    def setUp(self):
        '''
        Create different requests with status pending.
        Creating simple and librarian user.
        Getting the jwt authentication token for librarian user.
        '''
        self.requests = UserBookRequestFactory.create_batch(BATCH_SIZE)
        self.url_name = 'request_detail'
        self.customer_user = UserFactory()
        self.librarian_user = UserFactory()
        librarian = Permission.objects.get(codename=LIBRARIAN_PERMISSION)
        self.librarian_user.user_permissions.add(librarian)
        self.librarian_user.save()

        data = {
            "username": self.librarian_user.username,
            "password": USER_PASSWORD
        }
        token = get_jwt_token(data)['token']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_get_request(self):
        '''Test to get a request using its id by a librarian user.'''
        response = self.client.get(
            reverse(self.url_name, args=[self.requests[0].id]),
            format=FORMAT
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['requested_book'], self.requests[0].requested_book.id)

    def test_get_request_with_wrong_id(self):
        '''Test to get request that doesnot exist.'''
        response = self.client.get(
            reverse(self.url_name, args=[1000]),
            format=FORMAT
            )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Not found.')

    def test_get_request_unauthorized(self):
        '''Test to get a request without authentication.'''
        self.client.credentials()
        response = self.client.get(
            reverse(self.url_name, args=[self.requests[0].id]),
            format=FORMAT
            )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_request_simple_user(self):
        '''Test to get a request with a simple user account.'''
        data = {
            "username": self.customer_user.username,
            "password": USER_PASSWORD
        }
        token = get_jwt_token(data)['token']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.get(
            reverse(self.url_name, args=[self.requests[0].id]),
            format=FORMAT
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_librarian_approve_request(self):
        '''Test to approve a user request by a librarian via id.'''
        response = self.client.put(
            reverse(self.url_name, args=[self.requests[0].id]),
            data={'status': APPROVED_STATUS},
            format=FORMAT
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], APPROVED_STATUS)

    def test_librarian_unauthorized_approve_request(self):
        '''Test to approve a request using ananymous user.'''
        self.client.credentials()
        response = self.client.put(
            reverse(self.url_name, args=[self.requests[0].id]),
            data={'status': APPROVED_STATUS},
            format=FORMAT
            )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_librarian_reject_request(self):
        '''Test to reject a user request by a librarian via id.'''
        response = self.client.put(
            reverse(self.url_name, args=[self.requests[0].id]),
            data={'status': REJECTED_STATUS},
            format=FORMAT
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], REJECTED_STATUS)

    def test_librarian_unauthorized_reject_request(self):
        '''Test to reject a user request by a simple user via id.'''
        self.client.credentials()
        response = self.client.put(
            reverse(self.url_name, args=[self.requests[0].id]),
            data={'status': REJECTED_STATUS},
            format=FORMAT
            )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_request_with_wrong_input(self):
        '''Test to send wrong input in the request body.'''
        response = self.client.put(
            reverse(self.url_name, args=[self.requests[0].id]),
            data={'status': 'Incorrect'},
            format=FORMAT
            )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_librarain_non_existant_request(self):
        '''Test to update a request that doesnot exist.'''
        response = self.client.put(
            reverse(self.url_name, args=[100]),
            data={"status": REJECTED_STATUS},
            format=FORMAT
            )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
