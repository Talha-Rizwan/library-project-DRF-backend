import factory
from home.models import Book

class BookFactory(factory.Factory):
    class Meta:
        model = Book

    name = factory.Faker('text', max_nb_chars=50)
    author_name = factory.Faker('name')
    publisher_name = factory.Faker('company')
    number_of_books = factory.Faker('random_int', min=1, max=100)
