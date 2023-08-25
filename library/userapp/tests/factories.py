from factory import django, Faker
from userapp.models import User
from django.contrib.auth.hashers import make_password 

class UserFactory(django.DjangoModelFactory):
    class Meta:
        model = User

    username = Faker('user_name')
    password = make_password('password123')
    full_name = Faker('text', max_nb_chars=50)
    phone = Faker('phone_number')
    gender = Faker('random_element', elements=('M', 'F'))
    role = Faker('random_element', elements=('C', 'L', 'A'))
