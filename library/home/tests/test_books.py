from django.contrib.auth.models import Permission

from rest_framework import status
from rest_framework.test import APITestCase

from home.serializers import BookSerializer
from home.tests.factories import BookFactory
from home.models import Book
from userapp.tests.factories import UserFactory
from userapp.utlis import get_jwt_token

class BookViewSetTestCase(APITestCase):

    def setUp(self):
        self.books = BookFactory.create_batch(10)
        self.customer_user = UserFactory()
        self.librarian_user = UserFactory()
        self.url = '/api/home/book-view-set/'
        librarian = Permission.objects.get(codename='is_librarian')
        self.librarian_user.user_permissions.add(librarian)
        self.librarian_user.save()
  
        data = {
            "username": self.librarian_user.username,
            "password": 'password123'
        }
        token = get_jwt_token(data)['data']['token']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        
    def test_list_books(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 10)


    def test_create_book(self):
        serializer = BookSerializer(BookFactory.build())
        data = serializer.data
        del data['cover_image']
        response = self.client.post(self.url, data=data, format='json')        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])


    def test_create_book_without_credentials(self):
        self.client.credentials()
        serializer = BookSerializer(BookFactory.build())
        data = serializer.data
        del data['cover_image']
        response = self.client.post(self.url, data=data, format='json')        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_create_book_with_customer_user(self):
        user = {
            "username": self.customer_user.username,
            "password": 'password123'
        }
        token = get_jwt_token(user)['data']['token']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        serializer = BookSerializer(BookFactory.build())
        data = serializer.data
        del data['cover_image']
        response = self.client.post(self.url, data=data, format='json')        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_retrieve_book(self):
        self.client.credentials()
        response = self.client.get(f'{self.url}{self.books[0].id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_retrieve_book_with_invalid_id(self):
        self.client.credentials()
        response = self.client.get(f'{self.url}100/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_update_book(self):
        serializer = BookSerializer(self.books[0])
        data = serializer.data
        data['name'] = "Updated Book Name"
        data["number_of_books"] = 10
        del data['cover_image']
        response = self.client.put(f'{self.url}{self.books[0].id}/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], 'Updated Book Name')
        self.assertEqual(response.data['number_of_books'], 10)


    def test_update_book_with_invalid_id(self):
        serializer = BookSerializer(self.books[0])
        data = serializer.data
        data['name'] = "Updated Book Name"
        data["number_of_books"] = 10
        del data['cover_image']
        response = self.client.put(f'{self.url}100/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_delete_book(self):
        response = self.client.delete(f'{self.url}{self.books[0].id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=1).exists())


    def test_delete_book_with_unauthorized_user(self):
        user = {
            "username": self.customer_user.username,
            "password": 'password123'
        }
        token = get_jwt_token(user)['data']['token']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.delete(f'{self.url}{self.books[0].id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_search_books(self): 
        url = f'{self.url}?name={self.books[0].name}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.books[0].id, response.data[0]['id'])


    def test_search_books_with_wrong_param(self): 
        url = f'{self.url}?wrong={self.books[0].name}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 10)
