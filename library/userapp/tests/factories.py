'''Factory classes to create instances of models in userapp.'''
from django.contrib.auth.hashers import make_password
from userapp.tests.constants import USER_PASSWORD
from factory import django, Faker
from userapp.models import User

class UserFactory(django.DjangoModelFactory):
    '''User Factory class to create instances of user model for testing purposes.'''
    class Meta:
        '''Using the model User.'''
        model = User

    username = Faker('user_name')
    password = make_password(USER_PASSWORD)
    full_name = Faker('text', max_nb_chars=50)
    phone = Faker('phone_number')
    gender = Faker('random_element', elements=('M', 'F'))
    