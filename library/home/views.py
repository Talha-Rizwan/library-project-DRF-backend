from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import BookSerializer
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

