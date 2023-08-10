from django.db.models import Q
from django.contrib.auth.hashers import make_password

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import BookSerializer, UserSerializer
from .models import Book

@api_view(['GET'])
def homePage(request):
    print(request.user)
    return Response({
        'status': 200,
        'message': 'Yes! it is working now'
    })

@api_view(['GET', 'POST'])
def book_list(request, format=None):
    '''To Create a new book or Get all the books'''

    if request.method == 'GET':
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


    if request.method == 'POST':
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
    

@api_view(['GET', 'PUT', 'DELETE'])
def book_detail(request, pk, format=None):
    '''To perform Get, Update and Delete operations on a single book by passing id.'''
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response (serializer.data)
    
    elif request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
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