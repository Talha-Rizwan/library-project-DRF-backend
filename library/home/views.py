'''views of all the home class requests on url api/'''
from django.db.models import Q
from django.http import Http404

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from home.serializers import BookSerializer, RequestSerializer
from home.models import Book, PendingRequest
from userapp.permissions import LibrarianAuthenticatedOrReadOnly, IsLibrarianAuthenticated


class BookViewSet(viewsets.ModelViewSet):
    '''CRUD operations for Books, user role has read only access.'''
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [LibrarianAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]

class GetBookByNameOrAuthor(generics.ListAPIView):
    '''To search books by Book name or Author name.'''
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        name = self.kwargs.get('name')
        return Book.objects.filter(Q(name__icontains=name) | Q(author_name__icontains=name))

class UserBookRequestView(APIView):
    '''List view of requests of a user'''
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        '''To get a user's issued books, pending request books and returned books.'''
        try:
            issued_books = PendingRequest.objects.filter(
                Q(request_user=request.user) & Q(status='A')
                )
            books_issued = []

            for book in issued_books:
                books_issued.append(book.requested_book.name)

            requested_books = PendingRequest.objects.filter(
                Q(request_user = request.user) & Q(status='P')
                )
            books_requested = []

            for book in requested_books:
                books_requested.append(book.requested_book.name)

            returned_books = PendingRequest.objects.filter(
                Q(request_user=request.user) & (Q(status='C') | Q(status='B'))
                )
            books_returned = []

            for book in returned_books:
                books_returned.append(book.requested_book.name)

            return Response({
                    'status': True,
                    'message': 'success data',
                    'data': {
                        'books': {
                            'issued books': books_issued,
                            'requested books': books_requested,
                            'returned books' : books_returned
                            }
                        }
            }, status= status.HTTP_200_OK)

        except Exception as error:
            print(error)
            return Response({
                'status': False,
                'message': 'something went wrong!'
            })

    def post(self, request):
        '''Authenticated user to create a new pending request.'''
        data = request.data
        data['status'] = 'P'
        data['request_user'] = request.user.id
        serializer = RequestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListBookRequestView(generics.ListAPIView):
    '''All the pending requests list view'''
    queryset = PendingRequest.objects.filter(status='P')
    serializer_class = RequestSerializer
    permission_classes = [IsLibrarianAuthenticated]
    authentication_classes = [JWTAuthentication]


class DetailBookRequestView(APIView):
    '''Librarian view to get or update user request'''
    permission_classes = [IsLibrarianAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self, pk):
        '''Returns requested pending request object if available'''
        try:
            return PendingRequest.objects.get(pk=pk)
        except PendingRequest.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''To get a specific user request.'''
        req = self.get_object(pk)
        serializer = RequestSerializer(req)
        return Response (serializer.data)

    def put(self, request, pk, format=None):
        '''Update the request status from Pending to Approved or Rejected.'''
        req = self.get_object(pk)

        request.data['requested_book'] = req.requested_book.id
        serializer = RequestSerializer(req, data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            if request.data['status'] == 'A':
                try:
                    book = Book.objects.get(pk=instance.requested_book.id)
                    book.number_of_books -= 1
                    book.save()
                except Exception as error:
                    print(error)

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReturnBookView(APIView):
    '''User view to initiate a return request.'''
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self, pk):
        '''Return specific request object if available'''
        try:
            return PendingRequest.objects.get(pk=pk)
        except PendingRequest.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        '''
        User method to request to return back the book 
        (needs to be approved by librarian)
        '''
        req = self.get_object(pk)
        request.data['requested_book'] = req.requested_book.id
        serializer = RequestSerializer(req, data=request.data)

        if req.request_user == request.user:
            request.data['status'] = 'B'

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {'message': 'the user is not authorized'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
            )

class CloseBookRequest(APIView):
    '''Librarian view to close a return book request.'''
    permission_classes = [IsLibrarianAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self, pk):
        '''Return requested request object if available'''
        try:
            return PendingRequest.objects.get(pk=pk)
        except PendingRequest.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        '''Librarian method to close a request if user has requested to close it.'''
        req = self.get_object(pk)
        serializer = RequestSerializer(req, data=request.data)

        if req.status == 'B':
            if serializer.is_valid():
                instance = serializer.save()

                if request.data['status'] == 'C':
                    try:
                        book = Book.objects.get(pk=instance.requested_book.id)
                        book.number_of_books += 1
                        book.save()
                    except Exception as error:
                        print(error)

                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {'message': 'User has not opened a closed request'},
            status=status.HTTP_406_NOT_ACCEPTABLE
            )
