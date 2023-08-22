'''All routes for the requests at api/home/ '''
from django.urls import path

from rest_framework.routers import DefaultRouter

from home import views

router = DefaultRouter()
router.register(r'book-view-set', views.BookViewSet, basename='book')


urlpatterns = [
    path('book-detail-name/<str:name>/', views.GetBookByNameOrAuthor.as_view(), name='book-detail-name'),
    path('user-request/', views.UserBookRequestView.as_view(), name='pending-request'),
    path('all-request/', views.ListBookRequestView.as_view(), name='all-request'),
    path('request/<int:pk>/', views.DetailBookRequestView.as_view(), name='request'),
    path('return-request/<int:pk>/', views.ReturnBookView.as_view(), name='return-request'),
    path('close-request/<int:pk>/', views.CloseBookRequest.as_view(), name='close-request'),
]
urlpatterns += router.urls
