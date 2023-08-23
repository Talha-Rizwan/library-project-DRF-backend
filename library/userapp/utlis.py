'''All utility functions for this app are available here.'''
from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken

def get_jwt_token(data):
    '''To get the jwt token for user authentication'''
    user = authenticate(username=data['username'], password=data['password'])

    if not user:
        return {'message': 'imvalid credentials', 'data': {}}
    refresh = RefreshToken.for_user(user)
    return {
        'message': 'login success',
        'data': {
            'token':{
                'refresh': str(refresh),
                'access': str(refresh.access_token)
                }
            }
        }
