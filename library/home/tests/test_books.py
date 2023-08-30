'''Test cases for the api/home/book-view-set/ api'''
from django.contrib.auth.models import Permission

from rest_framework import status
from rest_framework.test import APITestCase

from home.serializers import BookSerializer
from home.tests.factories import BookFactory
from home.models import Book
from home.tests.constants import BATCH_SIZE, FORMAT
from userapp.tests.factories import UserFactory
from userapp.utlis import get_jwt_token

class BookViewSetTestCase(APITestCase):
    '''Class to test the View of BookViewSet using the url api/home/book-view-set/'''
    def setUp(self):
        '''
        setUp class create a batch of book instances, 
        crete a simple user and a user with is_librarian permission.
        send credentials and get jwt token to make requests.
        '''
        self.books = BookFactory.create_batch(BATCH_SIZE)
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
        token = get_jwt_token(data)['token']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_list_books(self):
        '''Test to list all books by anonyous user'''
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), BATCH_SIZE)

    def test_create_book(self):
        '''Test to crete new book using librarian user.'''
        serializer = BookSerializer(BookFactory.build())
        data = serializer.data
        del data['cover_image']
        response = self.client.post(self.url, data=data, format=FORMAT)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])

    def test_create_book_without_credentials(self):
        '''Test to create book using an anonymous user.'''
        self.client.credentials()
        serializer = BookSerializer(BookFactory.build())
        data = serializer.data
        del data['cover_image']
        response = self.client.post(self.url, data=data, format=FORMAT)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_with_customer_user(self):
        '''Test to create user with customer user.'''
        user = {
            "username": self.customer_user.username,
            "password": 'password123'
        }
        token = get_jwt_token(user)['token']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        serializer = BookSerializer(BookFactory.build())
        data = serializer.data
        del data['cover_image']
        response = self.client.post(self.url, data=data, format=FORMAT)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_book(self):
        '''Test to get a book by passing book id using anonymous user.'''
        self.client.credentials()
        response = self.client.get(f'{self.url}{self.books[0].id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_retrieve_book_with_invalid_id(self):
        '''Test to get a book with its id that doesnot exist.'''
        self.client.credentials()
        response = self.client.get(f'{self.url}100/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_update_book(self):
        '''Test to update a book by a librarian user using put method.'''
        serializer = BookSerializer(self.books[0])
        data = serializer.data
        data['name'] = "Updated Book Name"
        data["number_of_books"] = 10
        del data['cover_image']
        response = self.client.put(f'{self.url}{self.books[0].id}/', data=data, format=FORMAT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], 'Updated Book Name')
        self.assertEqual(response.data['number_of_books'], 10)


    def test_update_book_with_invalid_id(self):
        '''Test tp update a book using id that doesnot exist.'''
        serializer = BookSerializer(self.books[0])
        data = serializer.data
        data['name'] = "Updated Book Name"
        data["number_of_books"] = 10
        del data['cover_image']
        response = self.client.put(f'{self.url}100/', data=data, format=FORMAT)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_delete_book(self):
        '''Test to delete a book using librarian user.'''
        response = self.client.delete(f'{self.url}{self.books[0].id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=1).exists())


    def test_delete_book_with_unauthorized_user(self):
        '''test to delete a book with a simple user (not librarian)'''
        user = {
            "username": self.customer_user.username,
            "password": 'password123'
        }
        token = get_jwt_token(user)['token']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.delete(f'{self.url}{self.books[0].id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_search_books(self):
        '''Test to search a book using its name by anonymous user.'''
        url = f'{self.url}?name={self.books[0].name}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.books[0].id, response.data[0]['id'])


    def test_search_books_with_wrong_param(self):
        '''test to search a book using wrong params in the url instead of name.'''
        url = f'{self.url}?wrong={self.books[0].name}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), BATCH_SIZE)
