'''All serializers for home application models'''
from django.db.models import Q

from rest_framework import serializers

from home.models import Book, PendingRequest

# pylint: disable=R0903
class BookSerializer(serializers.ModelSerializer):
    '''Generic serializer for book model'''
    class Meta:
        '''The model class associated with this serializer is Book and includes all fields'''
        model = Book
        fields = ['id', 'name', 'author_name', 'publisher_name', 'number_of_books', 'cover_image']



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
            if len(PendingRequest.objects.filter(
                Q(request_user=request_user) & Q(status='A'))) >=3:
                raise serializers.ValidationError('The user already has 3 or more issued books.')
            if not request_book.number_of_books > 0:
                raise serializers.ValidationError('No copies of the book are available.')
        return data
