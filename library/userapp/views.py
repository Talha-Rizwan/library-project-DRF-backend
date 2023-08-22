'''Views of all the userapp class requests on url api/user/'''
from django.contrib.auth.hashers import make_password
from django.db.utils import IntegrityError

from rest_framework import generics
from rest_framework.exceptions import ValidationError
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
    '''Create or update user profile.'''
    permission_classes_post = []
    permission_classes_put = [IsAuthenticated]
    authentication_classes_put = [JWTAuthentication]

    def post(self, request):
        '''To register as a new user.'''
        try:
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
        '''To update user profile details.'''
        try:
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

        except ValidationError as validation_error:
            return Response({
                'data': validation_error.detail,
                'message': 'Validation failed'
            }, status=status.HTTP_400_BAD_REQUEST)

        except IntegrityError:
            return Response({
                'data': {},
                'message': 'Database integrity error'
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
        '''Post request with correct credintials will return a jwt token.'''
        try:
            data = request.data
            serializer = UserLoginSerializer(data=data)

            serializer.is_valid(raise_exception=True)
            response = get_jwt_token(serializer.data)

            return Response(response, status=status.HTTP_200_OK)

        except ValidationError as validation_error:
            return Response({
                'data': validation_error.detail,
                'message': 'Validation failed'
            }, status=status.HTTP_400_BAD_REQUEST)

        except IntegrityError:
            return Response({
                'data': {},
                'message': 'Database integrity error'
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            print(error)
            return Response({
                'data': {},
                'message': 'Something went wrong'
            }, status=status.HTTP_400_BAD_REQUEST)

class UserRoleListView(generics.ListAPIView):
    '''For getting all the users available with roles. (only librarian/admin)'''
    queryset = User.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [IsLibrarianAuthenticated]
    authentication_classes = [JWTAuthentication]

class LibrarianRoleDetailView(generics.RetrieveUpdateAPIView):
    '''Detail view of user with role via id'''
    queryset = User.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [ IsAdminAuthenticated]
    authentication_classes = [JWTAuthentication]
