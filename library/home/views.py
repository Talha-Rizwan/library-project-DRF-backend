from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import BookSerializer

@api_view(['GET'])
def homePage(request):
    print(request.user)
    return Response({
        'status': 200,
        'message': 'Yes! it is working now'
    })

@api_view(['POST'])
def post_book(request):
    try:
        data = request.data
        print('the request data is :', request.data)
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
