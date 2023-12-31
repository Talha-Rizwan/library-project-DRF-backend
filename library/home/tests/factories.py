'''Factory classes to create instances of models in home application.'''
from factory import django, Faker, SubFactory
from home.models import Book, PendingRequest
from home.constants import PENDING_STATUS
from userapp.tests.factories import UserFactory

class BookFactory(django.DjangoModelFactory):
    '''
    BookFactory class to create instances of Book model
    with ramdom values fulfilling the criteria.
    '''
    class Meta:
        '''Using the model Book for this class.'''
        model = Book

    name = Faker('text', max_nb_chars=50)
    author_name = Faker('name')
    publisher_name = Faker('company')
    number_of_books = Faker('random_int', min=1, max=100)

class UserBookRequestFactory(django.DjangoModelFactory):
    '''
    Class to create instances of PendingRequest model in the home application
    The default status is always pending.
    It creates user and books using the UserFactory and BookFactory
    as SubFactories to fill the required fields.
    '''
    class Meta:
        '''Using the model PendingRequest for this factory class.'''
        model = PendingRequest
    status = PENDING_STATUS
    requested_book = SubFactory(BookFactory)
    request_user = SubFactory(UserFactory)
