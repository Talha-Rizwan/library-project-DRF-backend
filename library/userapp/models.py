'''Models of Userapp application.'''
from django.db import models
from django.contrib.auth.models import AbstractUser

from userapp.constants import GENDER_CHOICES, ROLE_CHOICES

class User(AbstractUser):
    '''
    User Class inherited from in-built AbstractUser 
    Class from django.contrib.auth.models
    '''
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)

    REQUIRED_FIELDS = []

    class Meta:
        '''Available permissions to have different powers in the app.'''
        permissions = [
            ('is_librarian', 'Is librarian or above')
        ]

    def __str__(self):
        return self.username
