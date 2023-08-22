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
    
    role = models.CharField(max_length=1, choices=ROLE_CHOICES, null=False, default='C')

    REQUIRED_FIELDS = []

    class Meta:
        permissions = [
            ('is_librarian', 'Is librarian or above'),
            ('is_admin', 'Is an admin')
        ]

    def __str__(self):
        return self.username