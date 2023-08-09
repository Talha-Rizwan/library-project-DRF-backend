from django.urls import path, include
from .views import homePage, post_book

urlpatterns = [
    path('', homePage, name='home'),
    path('book',post_book, name='book' )
]
