'''Tests to return back a book by trying to close a book request by user.'''
from rest_framework import status
from rest_framework.test import APITestCase

from home.tests.factories import UserBookRequestFactory
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
        self.Requests = UserBookRequestFactory()
        self.customer_user = self.Requests.request_user
        self.Requests.request_user = self.customer_user
        self.Requests.status = 'A'
        self.Requests.save()
        self.url = '/api/home/return-request/'
  
        data = {
            "username": self.customer_user.username,
            "password": 'password123'
        }
        token = get_jwt_token(data)['data']['token']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        
    def test_request_to_close_by_user_owner(self):
        '''Test to change status of request to B by the owner account.'''
        response = self.client.put(f'{self.url}{self.Requests.id}/',data={"status": "B"}, format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'B')
    
    def test_request_to_close_by_not_owner(self):
        '''Test to change status of request to B by not the owner account.'''
        self.another_customer_user = UserFactory()
        
        data = {
            "username": self.another_customer_user.username,
            "password": 'password123'
        }
        token = get_jwt_token(data)['data']['token']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.put(f'{self.url}{self.Requests.id}/',data={"status": "B"}, format='json')
        self.assertEqual(response.status_code,status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.data['message'], "the user is not authorized or request is currently not approved." )

    def test_request_to_close_by_anonymous_user(self):
        '''Test to change status of request to B by anonymous user.'''
        self.client.credentials()
        response = self.client.put(f'{self.url}{self.Requests.id}/',data={"status": "B"}, format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], "Authentication credentials were not provided.")

    def test_request_not_exist(self):
        '''Test to update status of request that doesnot exist.'''
        response = self.client.put(f'{self.url}10/',data={"status": "B"}, format='json')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], "Not found.")

    def test_request_to_close_not_approved(self):
        '''Test to close a request that is not already approved by the librarian.'''
        self.Requests.status = 'P'
        self.Requests.save()
        response = self.client.put(f'{self.url}{self.Requests.id}/',data={"status": "B"}, format='json')
        self.assertEqual(response.status_code,status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.data['message'], "the user is not authorized or request is currently not approved." )
