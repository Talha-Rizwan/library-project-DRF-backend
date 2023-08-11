from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import BookSerializer, UserSerializer, UserLoginSerializer
from .models import Book
from .permissions import AdminAuthenticatedOrReadOnly


class book_list(APIView):
    '''To Create a new book or Get all the books'''
    permission_classes = [AdminAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        try:
            data = Book.objects.all()
            serializer = BookSerializer(data, many=True)
            return Response({
                    'status': True,
                    'message': 'success data',
                    'data': serializer.data
            }, status= status.HTTP_200_OK)
            
        except Exception as e:
            print(e)
            return Response({
                'status': False,
                'message': 'something went wrong!'
            })

    def post(self, request):
        try:
            data = request.data
            serializer = BookSerializer(data=data)
            if serializer.is_valid():
                serializer.save()

                return Response({
                    'status': True,
                    'message': 'success data',
                    'data': serializer.data
                })
                
            return Response({
                'status': False,
                'message': 'invalid data',
                'data': serializer.errors
            })
        
        except Exception as e:
            print(e)
            return Response({
                'status': False,
                'message': 'something went wrong!'
            })
    

class book_detail(APIView):
    '''To perform Get, Update and Delete operations on a single book by passing id.'''
    permission_classes = [AdminAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]
    
    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        book = self.get_object(pk)
        serializer = BookSerializer(book)
        return Response (serializer.data)
    
    def put(self, request, pk, format=None):
        book = self.get_object(pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        book = self.get_object(pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_book_by_name_or_author(request, name, format=None):
    '''To search book by Book name or Author name.'''
    try:
        books = Book.objects.filter(Q(name__icontains=name) | Q(author_name__icontains=name))
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


class RegisterView(APIView):

    def post(self, request):
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
        
        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message': 'something went wrong'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # TO-DO user update profile


class LoginView(APIView):

    def post(self, request):
        try:
            data = request.data
            serializer = UserLoginSerializer(data=data)

            if not serializer.is_valid():
                return Response({
                    'data': {},
                    'message': 'something went wrong'
                }, status=status.HTTP_400_BAD_REQUEST)
            response = serializer.get_jwt_token(serializer.data)

            return Response(response, status=status.HTTP_200_OK)  

        
        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message': 'something went wrong'
            }, status=status.HTTP_400_BAD_REQUEST)



