'''views of all the home class requests on url api/'''
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.http import Http404
from django.db.utils import IntegrityError

from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from home.serializers import BookSerializer, UserSerializer, UserLoginSerializer
from home.serializers import RequestSerializer, UserRoleSerializer
from home.models import Book, PendingRequest, User
from home.permissions import LibrarianAuthenticatedOrReadOnly
from home.permissions import IsLibrarianAuthenticated, IsAdminAuthenticated
from home.utils import get_jwt_token

class UserProfileView(APIView):
    '''create or update user profile.'''
    permission_classes_post = []
    permission_classes_put = [IsAuthenticated]
    authentication_classes_put = [JWTAuthentication]

    def post(self, request):
        '''to register as a new user'''
        try:
            data = request.data
            password = data.get('password')
            hashed_password = make_password(password)
            data['password'] = hashed_password
            serializer = UserSerializer(data=data)
            serializer = UserSerializer(data=data)

            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'validation failed'
                }, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()

            return Response({
                'data': {},
                'message': 'your account is created'
            }, status=status.HTTP_201_CREATED)

        except ValidationError as validation_error:
            return Response({
                'data': validation_error.detail,
                'message': 'validation failed'
            }, status=status.HTTP_400_BAD_REQUEST)

        except IntegrityError:
            return Response({
                'data': {},
                'message': 'database integrity error'
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            print(error)
            return Response({
                'data': {},
                'message': 'something went wrong'
            }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        '''to update user profile info.'''
        try:
            user = request.user
            data = request.data
            data.pop('username', None)
            data.pop('password', None)
            serializer = UserSerializer(user, data=data, partial=True)

            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'Validation failed'
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()

            return Response({
                'data': {},
                'message': 'Your profile has been updated'
            }, status=status.HTTP_200_OK)

        except ValidationError as validation_error:
            return Response({
                'data': validation_error.detail,
                'message': 'validation failed'
            }, status=status.HTTP_400_BAD_REQUEST)

        except IntegrityError:
            return Response({
                'data': {},
                'message': 'database integrity error'
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            print(error)
            return Response({
                'data': {},
                'message': 'Something went wrong'
            }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    '''To make a user login (get jwt token)'''

    def post(self, request):
        '''post request with correct credintials will return a jwt token.'''
        try:
            data = request.data
            serializer = UserLoginSerializer(data=data)

            if not serializer.is_valid():
                return Response({
                    'data': {},
                    'message': 'something went wrong'
                }, status=status.HTTP_400_BAD_REQUEST)
            response = get_jwt_token(serializer.data)

            return Response(response, status=status.HTTP_200_OK)

        except ValidationError as validation_error:
            return Response({
                'data': validation_error.detail,
                'message': 'validation failed'
            }, status=status.HTTP_400_BAD_REQUEST)

        except IntegrityError:
            return Response({
                'data': {},
                'message': 'database integrity error'
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            print(error)
            return Response({
                'data': {},
                'message': 'something went wrong'
            }, status=status.HTTP_400_BAD_REQUEST)


class UserRoleListView(APIView):
    '''for getting all the users available with roles. (only librarian/admin)'''
    permission_classes = [IsLibrarianAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        '''method for librarian/admin to get all the users with roles.'''
        try:
            data = User.objects.all()
            serializer = UserRoleSerializer(data, many=True)
            return Response({
                    'status': True,
                    'message': 'success data',
                    'data': serializer.data
            }, status= status.HTTP_200_OK)

        except ValidationError as validation_error:
            return Response({
                'data': validation_error.detail,
                'message': 'validation failed'
            }, status=status.HTTP_400_BAD_REQUEST)

        except IntegrityError:
            return Response({
                'data': {},
                'message': 'database integrity error'
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            print(error)
            return Response({
                'status': False,
                'message': 'something went wrong!'
            })


class LibrarianRoleDetailView(APIView):
    '''Detail view of user with role via id'''
    permission_classes = [IsAdminAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self, pk):
        '''return user object of given id if available'''
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''method for admin to get a perticular user with its role'''
        user = self.get_object(pk)
        serializer = UserRoleSerializer(user)
        return Response (serializer.data)

    def put(self, request, pk, format=None):
        '''method for admin to change the role of any user.'''
        user = self.get_object(pk)
        serializer = UserRoleSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookViewSet(viewsets.ModelViewSet):
    '''CRUD operations for Books, user role has read only access.'''
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [LibrarianAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]


class get_book_by_name_or_author(APIView):
    '''To search book by Book name or Author name.'''
    def get(self, request, name, format=None):
        try:
            books = Book.objects.filter(Q(name__icontains=name) | Q(author_name__icontains=name))
            serializer = BookSerializer(books, many=True)
            return Response(serializer.data)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UserBookRequestView(APIView):
    '''list view of requests of a user'''
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        '''To get a user's issued books, pending request books and returned books.'''
        try:
            issued_books = request.user.issued_books.all()
            books_issued = []

            for book in issued_books:
                books_issued.append(book.name)

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
                            "issued books": books_issued,
                            "requested books": books_requested,
                            "returned books" : books_returned
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


class ListBookRequestView(APIView):
    '''list view of requests (for librarian/admin only)'''
    permission_classes = [IsLibrarianAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        '''get all the pending requests.'''
        try:
            data = PendingRequest.objects.filter(status="P")
            serializer = RequestSerializer(data, many=True)
            return Response({
                    'status': True,
                    'message': 'success data',
                    'data': serializer.data
            }, status= status.HTTP_200_OK)

        except Exception as error:
            print(error)
            return Response({
                'status': False,
                'message': 'something went wrong!'
            })


class DetailBookRequestView(APIView):
    '''librarian view to get or update user request'''
    permission_classes = [IsLibrarianAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self, pk):
        '''returns requested pending request object if available'''
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
        '''update the request status from Pending to Approved or Rejected.'''
        req = self.get_object(pk)

        request.data['requested_book'] = req.requested_book.id
        serializer = RequestSerializer(req, data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            if request.data['status'] == 'A':
                try:
                    book = Book.objects.get(pk=instance.requested_book.id)
                    instance.request_user.issued_books.add(book)
                    book.number_of_books -= 1
                    book.save()
                except Exception as error:
                    print(error)

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReturnBookView(APIView):
    '''user view to initiate a return request.'''
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self, pk):
        '''return specific request object if available'''
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
            {'message': "the user is not authorized"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
            )


class CloseBookRequest(APIView):
    '''Librarian view to close a return book request.'''
    permission_classes = [IsLibrarianAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self, pk):
        '''return requested request object if available'''
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
                        instance.request_user.issued_books.remove(book)
                        book.number_of_books += 1
                        book.save()
                    except Exception as error:
                        print(error)

                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"message": "user has not opened a closed request"},
            status=status.HTTP_406_NOT_ACCEPTABLE
            )
