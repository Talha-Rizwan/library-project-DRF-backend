'''Views of all the userapp class requests on url api/user/'''
from django.contrib.auth.hashers import make_password

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from userapp.serializers import UserLoginSerializer, UserSerializer, UserRoleSerializer
from userapp.models import User
from userapp.permissions import IsLibrarianAuthenticated, IsAdminAuthenticated
from userapp.utlis import get_jwt_token


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
            'data': {},
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
            'data': {},
            'message': 'Your profile has been updated'
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

        return Response(response, status=status.HTTP_200_OK)


class UserRoleListView(generics.ListAPIView):
    '''
    For getting all the users available with roles. 
    permission only for librarian/admin
    '''
    queryset = User.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [IsLibrarianAuthenticated]
    authentication_classes = [JWTAuthentication]

class LibrarianRoleDetailView(generics.RetrieveUpdateAPIView):
    '''
    Detail view of user with role via id
    Only permission for admin.
    Admin can update a user role to librarian py its id.
    '''
    queryset = User.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [ IsAdminAuthenticated]
    authentication_classes = [JWTAuthentication]
