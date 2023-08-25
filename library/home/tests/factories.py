from factory import django, Faker, SubFactory
from home.models import Book, PendingRequest
from userapp.tests.factories import UserFactory
class BookFactory(django.DjangoModelFactory):
    class Meta:
        model = Book

    name = Faker('text', max_nb_chars=50)
    author_name = Faker('name')
    publisher_name = Faker('company')
    number_of_books = Faker('random_int', min=1, max=100)

class UserBookRequestFactory(django.DjangoModelFactory):
    class Meta:
        model = PendingRequest
    status = 'P'
    requested_book = SubFactory(BookFactory)
    request_user = SubFactory(UserFactory)
    