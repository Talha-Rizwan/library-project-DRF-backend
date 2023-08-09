from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    User Class inherited from in-built AbstractUser 
    Class from django.contrib.auth.models
    """
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    gender_choices = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=gender_choices, blank=True, null=True)

    role_choices = (
        ('A', 'Admin'),
        ('L', 'Librarian'),
        ('C', 'Customer'),
    )
    role = models.CharField(max_length=1, choices=role_choices, null=False, default='C')

    REQUIRED_FIELDS = []


    def __str__(self):
        return self.username

class Book(models.Model):
    name = models.CharField(max_length=50)
    author_name = models.CharField(max_length=50)
    publisher_name = models.CharField(max_length=50)
    number_of_books = models.PositiveIntegerField()
    
    #To-Do : Add the image field  

    def __str__(self):
        return self.name
