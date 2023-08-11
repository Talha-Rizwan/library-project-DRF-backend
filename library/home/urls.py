from django.urls import path
from home import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('book-list/',views.book_list.as_view(), name='book-list' ),
    path('book-detail/<int:pk>/',views.book_detail.as_view(), name='book-detail' ),
    path('book-detail-name/<str:name>/', views.get_book_by_name_or_author, name='book-detail-name'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),

]
urlpatterns = format_suffix_patterns(urlpatterns)
