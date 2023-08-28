'''Views of all the home class requests on url api/'''
from django.db.models import Q
from django.http import Http404

from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from home.serializers import BookSerializer, RequestSerializer, UserBookRequestSerializer
from home.models import Book, PendingRequest
from userapp.permissions import LibrarianAuthenticatedOrReadOnly, IsLibrarianAuthenticated


class BookViewSet(viewsets.ModelViewSet):
    '''
    CRUD operations for Books. 
    User role has read only access.
    '''
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [LibrarianAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def list(self, request):
        '''
        Search books by Book name or Author name.
        No authentication required.
        '''
        name = request.query_params.get('name')

        if name:
            books = Book.objects.filter(Q(name__icontains=name) | Q(author_name__icontains=name))
            serializer = BookSerializer(books, many=True)
            return Response(serializer.data)

        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response({
            "message": "No search parameters were provided",
            "data":serializer.data
        })


class UserBookRequestView(APIView):
    '''View of requests of the logged in user'''
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        '''
        Authenticated user can view all his issued, requested and returned books.
        '''
        issued_books = PendingRequest.objects.filter(
            request_user=request.user, status='A'
        ).values_list('requested_book__name', flat=True)

        requested_books = PendingRequest.objects.filter(
            request_user=request.user, status='P'
        ).values_list('requested_book__name', flat=True)

        returned_books = PendingRequest.objects.filter(
            Q(request_user=request.user, status='C') |
            Q(request_user=request.user, status='B')
        ).values_list('requested_book__name', flat=True)

        data = {
            'issued_books': issued_books,
            'requested_books': requested_books,
            'returned_books': returned_books
        }

        serializer = UserBookRequestSerializer(data)
        return Response({
            'status': True,
            'message': 'success data',
            'data': {
                'books': serializer.data
            }
        }, status=status.HTTP_200_OK)

    def post(self, request):
        '''Authenticated user to create a new pending request for a book.'''
        try:
            Book.objects.get(pk=request.data['requested_book'])
        except Book.DoesNotExist:
            raise Http404

        data = request.data
        data['status'] = 'P'
        data['request_user'] = request.user.id
        serializer = RequestSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ListBookRequestView(generics.ListAPIView):
    '''
    All the pending requests list view
    Only for Librarian/Admin
    '''
    queryset = PendingRequest.objects.filter(status='P')
    serializer_class = RequestSerializer
    permission_classes = [IsLibrarianAuthenticated]
    authentication_classes = [JWTAuthentication]


class DetailBookRequestView(generics.RetrieveUpdateAPIView):
    '''Librarian view to get or update user request'''
    queryset = PendingRequest.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [IsLibrarianAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_update(self, serializer):
        instance = serializer.save()

        if serializer.validated_data.get('status') == 'A':
            try:
                instance.requested_book.number_of_books -= 1
                instance.requested_book.save()
            except Exception as error:
                print(error)


class UserReturnBookView(generics.UpdateAPIView):
    '''
    User view to initiate a return request.
    User can only request to return their own request.
    '''
    queryset = PendingRequest.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self, pk):
        try:
            return PendingRequest.objects.get(pk=pk)
        except PendingRequest.DoesNotExist:
            raise Http404

    def update(self, request, pk, format=None):
        req = self.get_object(pk)

        if req.request_user == request.user and req.status == 'A':
            request.data['status'] = 'B'
            serializer = self.get_serializer(req, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)

        return Response(
            {'message': 'The user is not authorized or the request is currently not approved.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


class CloseBookRequest(APIView):
    '''
    Librarian view to close a return book request.
    Exclusive to librarian/admin only.
    '''
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
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()

            if request.data['status'] == 'C':

                try:
                    instance.requested_book.number_of_books +=1
                    instance.requested_book.save()
                except Exception as error:
                    print(error)

            return Response(serializer.data)
        return Response(
            {'message': 'User has not opened a closed request'},
            status=status.HTTP_406_NOT_ACCEPTABLE
        )
