from django.urls import path
from home import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('book-list/',views.book_list.as_view(), name='book-list' ),
    path('book-detail/<int:pk>/',views.book_detail.as_view(), name='book-detail' ),
    path('book-detail-name/<str:name>/', views.get_book_by_name_or_author, name='book-detail-name'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('update-profile/', views.UpdateUser.as_view(), name='update-profile'),
    path('pending-request/', views.BookRequestView.as_view(), name='pending-request'),
    path('all-request/', views.LibrarianBookRequestView.as_view(), name='all-request'),

]
urlpatterns = format_suffix_patterns(urlpatterns)
