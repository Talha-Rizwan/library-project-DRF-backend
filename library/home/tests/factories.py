from factory import django, Faker
from home.models import Book

class BookFactory(django.DjangoModelFactory):
    class Meta:
        model = Book

    name = Faker('text', max_nb_chars=50)
    author_name = Faker('name')
    publisher_name = Faker('company')
    number_of_books = Faker('random_int', min=1, max=100)
