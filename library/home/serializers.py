'''All serializers for home application models'''
from rest_framework import serializers

from home.models import Book, User, PendingRequest

# pylint: disable=R0903
class BookSerializer(serializers.ModelSerializer):
    '''Generic serializer for book model'''
    class Meta:
        '''The model class associated with this serializer is Book and includes all fields'''
        model = Book
        fields = ['id', 'name', 'author_name', 'publisher_name', 'number_of_books', 'cover_image']

# pylint: disable=R0903
class UserSerializer(serializers.ModelSerializer):
    '''Generic user serializer for user model'''
    class Meta:
        '''The model class associated with this serializer is User and includes certain fields'''
        model = User
        fields = ['username', 'password', 'full_name', 'phone', 'gender']

class UserLoginSerializer(serializers.Serializer):
    '''user serializer specific for login functionality'''
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


class RequestSerializer(serializers.ModelSerializer):
    '''generic pending request class serializer'''
    class Meta:
        '''
        The model class associated with this serializer is
        PendingRequest and includes all fields
        '''
        model = PendingRequest
        fields = ['request_user', 'requested_book', 'created', 'status']

    def validate(self, data):
        '''
        user request validation for issued books not more than 3 
        and requested book copy is available.
        '''
        is_creation = self.instance is None

        request_user = data.get('request_user')
        request_book = data.get('requested_book')
        if is_creation:
            if request_user and request_user.issued_books.count() >= 3:
                raise serializers.ValidationError('The user already has 3 or more issued books.')
            if not request_book.number_of_books > 0:
                raise serializers.ValidationError('No copies of the book are available.')
        return data
