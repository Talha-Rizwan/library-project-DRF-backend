from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def homePage(request):
    print(request.user)
    return Response({
        'status': 200,
        'message': 'Yes! it is working now'
    })