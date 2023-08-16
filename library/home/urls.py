from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from home import views

urlpatterns = [
    path('book-list/',views.book_list.as_view(), name='book-list' ),
    path('book-detail/<int:pk>/',views.book_detail.as_view(), name='book-detail' ),
    path('book-detail-name/<str:name>/', views.get_book_by_name_or_author, name='book-detail-name'),
    path('user-profile/', views.RegisterView.as_view(), name='user-profile'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('user-request/', views.UserBookRequestView.as_view(), name='pending-request'),
    path('all-request/', views.ListBookRequestView.as_view(), name='all-request'),
    path('request/<int:pk>/', views.DetailBookRequestView.as_view(), name='request'),
    path('return-request/<int:pk>/', views.ReturnBookView.as_view(), name='return-request'),
    path('close-request/<int:pk>/', views.CloseBookRequest.as_view(), name='close-request'),
    path('user-role/<int:pk>/',views.LibrarianRoleDetailView.as_view(), name='user-role'),
    path('users/', views.UserRoleListView.as_view(), name='users'),

]
urlpatterns = format_suffix_patterns(urlpatterns)
