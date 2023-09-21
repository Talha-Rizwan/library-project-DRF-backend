'''Views of all the userapp class requests on url api/user/'''
from django.contrib.auth.hashers import make_password

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from userapp.serializers import UserLoginSerializer, UserSerializer
from userapp.utlis import get_jwt_token
from userapp.models import User

class UserProfileView(APIView):
    '''View to create a new or update an existing user profile.'''
    permission_classes_post = []
    permission_classes_put = [IsAuthenticated]
    authentication_classes_put = [JWTAuthentication]

    def post(self, request):
        '''
        To register as a new user.
        No authentication for this required.
        '''
        data = request.data
        password = data.get('password')
        data['password'] = make_password(password)
        serializer = UserSerializer(data=data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'message': 'your account is created'
        }, status=status.HTTP_201_CREATED)


    def put(self, request):
        '''
        To update user profile details.
        User must be logged in and can only update their own profile.
        '''
        user = request.user
        data = request.data
        data.pop('username', None)
        data.pop('password', None)
        serializer = UserSerializer(user, data=data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'message': 'Your profile is updated successfully'
        }, status=status.HTTP_200_OK)


class LoginView(APIView):
    '''
    To make a user login using the jwt authentication
    only with correct credintials
    '''

    def post(self, request):
        '''Post request with correct credintials will return a jwt token.'''
        data = request.data
        serializer = UserLoginSerializer(data=data)

        serializer.is_valid(raise_exception=True)
        
        response = get_jwt_token(serializer.data)
        response['librarian'] = False
        newUser = User.objects.get(username=data['username'])
        user_permissions = newUser.user_permissions.all()
        for permission in user_permissions:
            if permission.codename == 'is_librarian':
                response['librarian'] = True
        return Response(response, status=status.HTTP_200_OK)
