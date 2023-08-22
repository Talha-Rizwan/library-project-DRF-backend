'''All routes for the requests at api/ '''
from django.urls import path

from userapp import views

urlpatterns = [
    path('user-profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('user-role/<int:pk>/',views.LibrarianRoleDetailView.as_view(), name='user-role'),
    path('users/', views.UserRoleListView.as_view(), name='users'),
]
