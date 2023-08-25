from django.contrib.auth.models import Permission

from rest_framework import status
from rest_framework.test import APITestCase

from home.tests.factories import BookFactory
from userapp.models import User
from home.models import Book

class BookViewSetTestCase(APITestCase):
    def setUp(self):
        self.books = BookFactory.create_batch(10)

        librarian = Permission.objects.get(codename='is_librarian')

        self.test_user = User.objects.create_user(
            username='testuser',
            password='testpassword',
        )
        self.test_user.user_permissions.add(librarian)
        self.test_user.save()
  
        url = '/api/user/login/'
        response = self.client.post(url,data={
            "username":'testuser',
            "password":'testpassword',
        }, format='json')
        self.token = response.data["data"]["token"]["access"]
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_books(self):
        url = '/api/home/book-view-set/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 10)

    def test_create_book(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        book_data = {
            "name": "The Chronicles of Narnia: The Lion...",
            "author_name": "C.S. Lewis",
            "publisher_name": "HarperCollins",
            "number_of_books": 10,
        }
        url = '/api/home/book-view-set/'
        response = self.client.post(url, data=book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    