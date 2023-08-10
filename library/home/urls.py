from django.urls import path, include
from .views import homePage, post_book

urlpatterns = [
    path('', homePage, name='home'),
    path('post-book',post_book, name='post-book' )
]
