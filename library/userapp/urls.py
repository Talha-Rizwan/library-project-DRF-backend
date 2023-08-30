'''All routes for the requests at api/user/ '''
from django.urls import path

from userapp import views

urlpatterns = [
    path('user-profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('login/', views.LoginView.as_view(), name='login'),
]
