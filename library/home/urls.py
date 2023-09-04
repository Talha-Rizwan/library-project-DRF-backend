'''All routes for the requests at api/home/ '''
from django.urls import path

from rest_framework.routers import DefaultRouter

from home import views

router = DefaultRouter()
router.register(r'book-view-set', views.BookViewSet, basename='book',)

urlpatterns = [
    path('user-request/', views.UserBookRequestView.as_view(), name='pending_request'),
    path('request/<int:pk>/', views.BookRequestView.as_view(), name='request_detail'),
    path('request/', views.BookRequestView.as_view(), name='request_list'),
    path('return-request/<int:pk>/', views.UserReturnBookView.as_view(), name='return_request'),
    path('close-request/<int:pk>/', views.CloseBookRequest.as_view(), name='close_request'),
]
urlpatterns += router.urls