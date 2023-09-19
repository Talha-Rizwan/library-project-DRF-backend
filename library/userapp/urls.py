'''All routes for the requests at api/user/ '''
from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from userapp import views

urlpatterns = [
    path('user-profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
