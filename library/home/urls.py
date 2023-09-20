'''All routes for the requests at api/home/ '''
from django.urls import path

from rest_framework.routers import DefaultRouter

from home import views

router = DefaultRouter()
router.register(r'book-view-set', views.BookViewSet, basename='book',)
router.register(r'delay-request', views.LibrarianDelayedBookReturnView, basename='delay-request')
router.register(r'request-set', views.UserBookRequests, basename='request-set',)


urlpatterns = [
    path('user-request/', views.UserBookRequestView.as_view(), name='pending_request'),
    path('request/<int:pk>/', views.BookRequestView.as_view(), name='request_detail'),
    path('request/', views.BookRequestView.as_view(), name='request_list'),
    path('return-request/<int:pk>/', views.UserReturnBookView.as_view(), name='return_request'),
    path('re-request/<int:pk>/', views.UserRerequestBookView.as_view(), name='re_request'),
    path('close-request/<int:pk>/', views.CloseBookRequest.as_view(), name='close_request'),
    path('ticket/', views.UserRequestTicket.as_view(), name='create-ticket'),
    path('librarian-ticket/<int:pk>/', views.LibrarianTicket.as_view(), name='librarian-ticket')
]
urlpatterns += router.urls
