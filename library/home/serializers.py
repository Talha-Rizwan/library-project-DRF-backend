from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .models import Book, User, PendingRequest

class BookSerializer(serializers.ModelSerializer):
    '''Generic serializer for book object'''
    class Meta:
        model = Book
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    '''Generic user serializer for user objects'''
    class Meta:
        model = User
        fields = ['username', 'password', 'full_name', 'phone', 'gender']

class UserLoginSerializer(serializers.Serializer):
    '''user serializer specific for login functionality'''
    username = serializers.CharField()
    password = serializers.CharField()

    def vaildate(self, data):

        if not User.objects.filter(username = data['username']).exists():
            raise serializers.ValidationError('account do not exist')
        return data
    
    def get_jwt_token(self, data):
        '''To get the jwt token for user authentication'''
        user = authenticate(username=data['username'], password=data['password'])

        if not user:
            return {'message': 'imvalid credentials', 'data': {}}
        refresh = RefreshToken.for_user(user)
        return {'message': 'login success', 'data': {'token': {'refresh': str(refresh),'access': str(refresh.access_token)}}}

class UserRoleSerializer(serializers.ModelSerializer):
    '''User serializer specific for user role functionality'''
    class Meta:
        model = User
        fields = ['id', 'username', 'role']


class PendingRequestSerializer(serializers.ModelSerializer):
    '''generic pending request class serializer'''
    # request_user = UserSerializer()
    # requested_book = BookSerializer()
    
    class Meta:
        model = PendingRequest
        fields = '__all__'
    
    def validate(self, data):
        request_user = data.get('request_user')
        request_book = data.get('requested_book')
        my_book = Book.objects.get(pk=request_book.id)

        if request_user and request_user.issued_books.count() >= 3:
            raise serializers.ValidationError("The user already has 3 or more issued books.")
        if not request_book.number_of_books > 0:
            raise serializers.ValidationError("No copies of the book are available at the moment.")
        return data

        
class ReturnRequestSerializer(serializers.ModelSerializer):
    '''serializer specific to closing request funcitonality'''
    class Meta:
        model = PendingRequest
        fields = '__all__' 
