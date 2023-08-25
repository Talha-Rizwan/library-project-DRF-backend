from django.contrib.auth.models import Permission

from rest_framework import status
from rest_framework.test import APITestCase

from home.serializers import BookSerializer
from home.tests.factories import BookFactory
from userapp.models import User
from home.models import Book
from userapp.tests.factories import UserFactory
from userapp.utlis import get_jwt_token

class BookViewSetTestCase(APITestCase):
    def setUp(self):
        self.books = BookFactory.create_batch(10)
        self.test_user = UserFactory()
        self.url = '/api/home/book-view-set/'

        librarian = Permission.objects.get(codename='is_librarian')
        self.test_user.user_permissions.add(librarian)
        self.test_user.save()
  
        data = {
            "username": self.test_user.username,
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


    def test_retrieve_book(self):
        self.client.credentials()
        response = self.client.get(f'{self.url}{self.books[0].id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


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


    def test_delete_book(self):
        response = self.client.delete(f'{self.url}{self.books[0].id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=1).exists())


    def test_search_books(self): 
        url = f'{self.url}?name={self.books[0].name}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.books[0].id, response.data[0]['id'])
