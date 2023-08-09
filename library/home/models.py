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

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def __str__(self):
        return self.username

class Book(models.Model):
    # name, image, author name, publisher and number of books
    name = models.CharField(max_length=50)
    author_name = models.CharField(max_length=50)
    publisher_name = models.CharField(max_length=50)
    number_of_books = models.PositiveIntegerField()
    #To-Do : Add the image field  

    def __str__(self):
        return self.name
