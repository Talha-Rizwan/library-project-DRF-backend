'''Serializers for the User model.'''
from rest_framework import serializers

from userapp.models import User

# pylint: disable=R0903
class UserSerializer(serializers.ModelSerializer):
    '''Generic user serializer for user model'''
    class Meta:
        '''The model class associated with this serializer is User and includes certain fields'''
        model = User
        fields = ['username', 'password', 'full_name', 'phone', 'gender']

class UserLoginSerializer(serializers.Serializer):
    '''User serializer specific for login functionality'''
    username = serializers.CharField()
    password = serializers.CharField()

    def vaildate(self, data):
        '''To validate the user exists or not.'''

        if User.objects.filter(username = data['username']).exists():
            return data
        
        raise serializers.ValidationError('account do not exist')
