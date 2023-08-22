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

        if not User.objects.filter(username = data['username']).exists():
            raise serializers.ValidationError('account do not exist')
        return data

# pylint: disable=R0903
class UserRoleSerializer(serializers.ModelSerializer):
    '''User serializer specific for user role functionality'''
    class Meta:
        '''The model class associated with this serializer is User and includes certain fields'''
        model = User
        fields = ['id', 'username', 'role']
