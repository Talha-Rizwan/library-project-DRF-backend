'''Views of all the home class requests on url api/'''
from django.db.models import Q
from django.http import Http404
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from datetime import timedelta
from django.utils import timezone


from rest_framework.decorators import action
from rest_framework import generics, status, viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from home.serializers import BookSerializer, RequestSerializer
from home.serializers import UserBookRequestSerializer, RequestTicketSerializer
from home.models import Book, PendingRequest, RequestTicket
from userapp.permissions import LibrarianAuthenticatedOrReadOnly, IsLibrarianAuthenticated
from home.constants import PENDING_STATUS, APPROVED_STATUS, RETURN_BACK_STATUS, REJECTED_STATUS
from home.constants import CLOSED_STATUS, LIBRARIAN_EMAIL, DELAYED_REQUEST_DAYS

class BookViewSet(viewsets.ModelViewSet):
    '''
    CRUD operations for Books. 
    User role has read only access.
    '''
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [LibrarianAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def list(self, request):
        '''
        Search books by Book name or Author name.
        No authentication required.
        '''
        name = request.query_params.get('name')

        if name:
            books = Book.objects.filter(Q(name__icontains=name) | Q(author_name__icontains=name))
            serializer = BookSerializer(books, many=True)
            return Response(serializer.data)

        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response({
            "message": "No search parameters were provided",
            "data":serializer.data
        })


class UserBookRequestView(APIView):
    '''View of requests of the logged in user'''
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        '''
        Authenticated user can view all his issued, requested and returned books.
        '''
        issued_books = PendingRequest.objects.filter(
            request_user=request.user, status=APPROVED_STATUS
        ).values_list('requested_book__name', flat=True)

        requested_books = PendingRequest.objects.filter(
            request_user=request.user, status=PENDING_STATUS
        ).values_list('requested_book__name', flat=True)

        returned_books = PendingRequest.objects.filter(
            Q(request_user=request.user, status=CLOSED_STATUS) |
            Q(request_user=request.user, status=RETURN_BACK_STATUS)
        ).values_list('requested_book__name', flat=True)

        data = {
            'issued_books': issued_books,
            'requested_books': requested_books,
            'returned_books': returned_books
        }

        serializer = UserBookRequestSerializer(data)
        return Response({
                'books': serializer.data
            }, status=status.HTTP_200_OK)

    def post(self, request):
        '''Authenticated user to create a new pending request for a book.'''
        try:
            Book.objects.get(pk=request.data['requested_book'])
        except Book.DoesNotExist:
            raise Http404

        data = request.data
        data['status'] = PENDING_STATUS
        data['request_user'] = request.user.id
        serializer = RequestSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class BookRequestView(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    '''
    All the pending requests Librarian view to get or update user requests
    Only for Librarian/Admin
    '''
    queryset = PendingRequest.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [IsLibrarianAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def perform_update(self, serializer):
        instance = serializer.save()

        if serializer.validated_data.get('status') == APPROVED_STATUS:
            try:
                instance.requested_book.number_of_books -= 1
                instance.requested_book.save()
            except PendingRequest.DoesNotExist:
                print('The request does not exist.')

class UserReturnBookView(generics.UpdateAPIView):
    '''
    User view to initiate a return request.
    User can only request to return their own request.
    '''
    queryset = PendingRequest.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def update(self, request, pk, format=None):
        req = self.get_object()

        if req.request_user == request.user and req.status == APPROVED_STATUS:
            request.data['status'] = RETURN_BACK_STATUS
            serializer = self.get_serializer(req, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)

        return Response(
            {'message': 'The user is not authorized or the request is currently not approved.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


class CloseBookRequest(generics.UpdateAPIView):
    '''
    Librarian view to close a return book request.
    Exclusive to librarian/admin only.
    '''
    queryset = PendingRequest.objects.all()
    permission_classes = [IsLibrarianAuthenticated]
    authentication_classes = [JWTAuthentication]

    def put(self, request, pk, format=None):
        '''Librarian method to close a request if user has requested to close it.'''
        req = self.get_object()
        serializer = RequestSerializer(req, data=request.data)

        if req.status == RETURN_BACK_STATUS:
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()

            if request.data['status'] == CLOSED_STATUS:

                try:
                    instance.requested_book.number_of_books +=1
                    instance.requested_book.save()
                except PendingRequest.DoesNotExist as error:
                    print(f'Request does not exist {error}')

            return Response(serializer.data)
        return Response(
            {'message': 'User has not opened a closed request'},
            status=status.HTTP_406_NOT_ACCEPTABLE
        )


class DelayRequestView(viewsets.ModelViewSet):
    """
    View to get all pending request objects older than 15 days.
    """
    queryset = PendingRequest.objects.filter(
        status= APPROVED_STATUS,
        created__lte=timezone.now() - timedelta(days=DELAYED_REQUEST_DAYS)
    )
    serializer_class = RequestSerializer
    permission_classes = [IsLibrarianAuthenticated]
    authentication_classes = [JWTAuthentication]

    @action(detail=True, methods=['post'])
    def send_mail(self, request, pk=None):
        try:
            pending_request = get_object_or_404(PendingRequest, pk=pk)

            subject = 'Delay Notification'
            message = f"Your booking for {pending_request.requested_book.name} book has been delayed."
            from_email = LIBRARIAN_EMAIL  
            recipient_list = [pending_request.request_user.email]

            send_mail(subject, message, from_email, recipient_list)
        except PendingRequest.DoesNotExist:
            return Response({'message': 'object doesnot exist'})

        return Response({'message': 'Email sent successfully'})


class UserRequestTicket(APIView):
    '''list view of requests of a user'''
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        '''get all the pending tickets only by librarian/admin.'''
        data = RequestTicket.objects.filter(status="P")
        if not request.user.has_perm('userapp.is_librarian'):
            return Response({
                'status': False,
                'message': 'you are not authorized'
            })
        serializer = RequestSerializer(data, many=True)
        return Response(serializer.data, status= status.HTTP_200_OK)


    def post(self, request):
        '''Authenticated user to create a new book ticket.'''
        data = request.data
        data['status'] = PENDING_STATUS
        data['request_user'] = request.user.id
        serializer = RequestTicketSerializer(data=data)
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        subject = 'Delay Notification'
        message = f"A new Book Ticket has been generated by {request.user} for book : {request.data['book_name']}"
        from_email = LIBRARIAN_EMAIL  
        recipient_list = ['librarian@gmail.com']

        send_mail(subject, message, from_email, recipient_list)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LibrarianTicket(APIView):
    '''Librarian view to close a return book request.'''
    permission_classes = [IsLibrarianAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self, pk):
        '''return requested ticket object if available'''
        try:
            return RequestTicket.objects.get(pk=pk)
        except RequestTicket.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        '''method for admin to get a perticular user generated ticket'''
        user = self.get_object(pk)
        serializer = RequestTicketSerializer(user)
        return Response (serializer.data)

    def put(self, request, pk, format=None):
        '''Librarian method to change status of ticket request.'''
        req = self.get_object(pk)
        data =request.data
        if request.data['status'] == REJECTED_STATUS:
            data['book_name'] = req.book_name
        serializer = RequestTicketSerializer(req, data=data)

        if req.status == PENDING_STATUS:
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()

            if request.data['status'] == APPROVED_STATUS:
                new_book = Book(
                name=request.data['book_name'],
                author_name=request.data['author_name'],
                publisher_name=request.data['publisher'],
                number_of_books=request.data['number_of_copies']
                )
                new_book.save()
                subject = 'Ticket Approve Notification'
                message = f"Your request ticket for book {instance.book_name} has been Approved."
                from_email = LIBRARIAN_EMAIL  
                recipient_list = ['user@gmail.com']

                send_mail(subject, message, from_email, recipient_list)

            elif req.status == REJECTED_STATUS:
                subject = 'Ticket Rejection Notification'
                message = f"Your request ticket for book {instance.book_name} has been rejected due to reason : {request.data['reason']}"
                from_email = LIBRARIAN_EMAIL  
                recipient_list = ['user@gmail.com']

                send_mail(subject, message, from_email, recipient_list)

            return Response(serializer.data)
        
        return Response(
            {"message": "This is not a pending ticket."},
            status=status.HTTP_406_NOT_ACCEPTABLE
        )
