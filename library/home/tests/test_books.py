from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from .factories import BookFactory
from userapp.models import User
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType



class BookViewSetTestCase(APITestCase):
    def setUp(self):

        user_content_type = ContentType.objects.get_for_model(User)
        user_permissions = Permission.objects.filter(content_type=user_content_type)        

        for permission in user_permissions:
            if permission.codename.startswith("is_librarian"):
                print(permission)
                librarian = permission

        self.test_user = User.objects.create_user(
            username='testuser',
            password='testpassword',
        )

       
        self.test_user.user_permissions.add(librarian)

        self.test_user.save()

        user_data = {
            "username":'testuser',
            "password":'testpassword',
            }
        url = '/api/user/login/'
        response = self.client.post(url,data=user_data, format='json')
        self.token = response.data["data"]["token"]["access"]
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_list_books(self):
        books = BookFactory.create_batch(10)
        for book in books:
            book.save()

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

