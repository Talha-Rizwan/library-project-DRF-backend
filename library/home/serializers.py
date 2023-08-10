from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .models import Book, User

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'full_name', 'phone', 'gender']

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def vaildate(self, data):

        if not User.objects.filter(username = data['username']).exists():
            raise serializers.ValidationError('account do not exist')
        return data
    
    def get_jwt_token(self, data):
        user = authenticate(username=data['username'], password=data['password'])

        if not user:
            return {'message': 'imvalid credentials', 'data': {}}
        
        refresh = RefreshToken.for_user(user)
        return {'message': 'login success', 'data': {'token': {'refresh': str(refresh),'access': str(refresh.access_token)}}}
 
