'''Tests to return back a book by trying to close a book request by user.'''
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from home.tests.factories import UserBookRequestFactory
from home.tests.constants import FORMAT
from home.constants import PENDING_STATUS, APPROVED_STATUS, RETURN_BACK_STATUS
from userapp.tests.constants import USER_PASSWORD
from userapp.tests.factories import UserFactory
from userapp.utlis import get_jwt_token

class UserReturnRequestTestCase(APITestCase):
    '''Class to evaluate all the scenarios of UserReturnBookView'''
    def setUp(self):
        '''
        Create Request with status approved.
        Creating simple user.
        Getting the jwt authentication token for user.
        '''
        self.request = UserBookRequestFactory()
        self.customer_user = self.request.request_user
        self.request.request_user = self.customer_user
        self.request.status = APPROVED_STATUS
        self.request.save()
        self.url_name = 'return_request'

        data = {
            "username": self.customer_user.username,
            "password": USER_PASSWORD
        }
        token = get_jwt_token(data)['token']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_request_to_close_by_user_owner(self):
        '''Test to change status of request to B by the owner account.'''
        response = self.client.put(
            reverse(self.url_name, args=[self.request.id]),
            data={'status': RETURN_BACK_STATUS},
            format=FORMAT
            )
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['status'], RETURN_BACK_STATUS)

    def test_request_to_close_by_not_owner(self):
        '''Test to change status of request to B by not the owner account.'''
        self.another_customer_user = UserFactory()

        data = {
            "username": self.another_customer_user.username,
            "password": USER_PASSWORD
        }
        token = get_jwt_token(data)['token']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.put(
            reverse(self.url_name, args=[self.request.id]),
            data={'status': RETURN_BACK_STATUS},
            format=FORMAT
            )
        self.assertEqual(response.status_code,status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(
            response.data['message'],
            "The user is not authorized or the request is currently not approved."
            )

    def test_request_to_close_by_anonymous_user(self):
        '''Test to change status of request to B by anonymous user.'''
        self.client.credentials()
        response = self.client.put(
            reverse(self.url_name, args=[self.request.id]),
            data={"status": RETURN_BACK_STATUS},
            format=FORMAT
            )
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], "Authentication credentials were not provided.")

    def test_request_not_exist(self):
        '''Test to update status of request that doesnot exist.'''
        response = self.client.put(
            reverse(self.url_name, args=[10]),
            data={"status": RETURN_BACK_STATUS},
            format=FORMAT
            )
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], "Not found.")

    def test_request_to_close_not_approved(self):
        '''Test to close a request that is not already approved by the librarian.'''
        self.request.status = PENDING_STATUS
        self.request.save()
        response = self.client.put(
            reverse(self.url_name, args=[self.request.id]),
            data={'status': RETURN_BACK_STATUS},
            format=FORMAT
            )
        self.assertEqual(response.status_code,status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(
            response.data['message'],
            "The user is not authorized or the request is currently not approved." 
            )
