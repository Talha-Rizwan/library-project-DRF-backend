'''All serializers for home application models'''
from rest_framework import serializers

from home.models import Book, PendingRequest, RequestTicket
from home.constants import APPROVED_STATUS
# pylint: disable=R0903
class BookSerializer(serializers.ModelSerializer):
    '''Generic serializer for book model'''
    class Meta:
        '''
        The model class associated with this serializer is Book and includes all fields
        '''
        model = Book
        fields = ['id', 'name', 'author_name', 'publisher_name', 'number_of_books', 'cover_image']


class UserBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendingRequest
        fields = ['id', 'requested_book', 'created', 'status']
        depth = 1

class RequestSerializer(serializers.ModelSerializer):
    '''Generic pending request class serializer'''
    class Meta:
        '''
        The model class associated with this serializer is
        PendingRequest and includes all fields
        '''
        model = PendingRequest
        fields = ['id', 'request_user', 'requested_book', 'created', 'status']

    def validate(self, attrs):
        '''
        User request validation for issued books not more than 3 
        and requested book copy is available.
        '''
        is_creation = self.instance is None

        request_user = attrs.get('request_user')
        request_book = attrs.get('requested_book')
        if is_creation:
            if PendingRequest.objects.filter(
                request_user=request_user, 
                status=APPROVED_STATUS
                ).count() >=3:
                raise serializers.ValidationError('The user already has 3 or more issued books.')
            if request_book.number_of_books == 0:
                raise serializers.ValidationError('No copies of the book are available.')
        return attrs

class UserBookRequestSerializer(serializers.Serializer):
    '''
    User request serializer to return attributes related to user.
    '''
    issued_books = serializers.ListField(child=serializers.CharField())
    requested_books = serializers.ListField(child=serializers.CharField())
    returned_books = serializers.ListField(child=serializers.CharField())

class RequestTicketSerializer(serializers.ModelSerializer):
    '''User serializer specific for user role functionality'''
    class Meta:
        '''The model class associated with this serializer is User and includes certain fields'''
        model = RequestTicket
        exclude = ['created', 'book_name']

class UserRequestTicketSerializer(serializers.ModelSerializer):
    '''User serializer specific for user role functionality'''
    class Meta:
        '''The model class associated with this serializer is User and includes certain fields'''
        model = RequestTicket
        exclude = ['created']
