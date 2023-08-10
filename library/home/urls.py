from django.urls import path
from .views import homePage, book_list, book_detail
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', homePage, name='home'),
    path('book-list',book_list, name='book-list' ),
    path('book-detail/<int:pk>/',book_detail, name='book-detail' )

]
urlpatterns = format_suffix_patterns(urlpatterns)
