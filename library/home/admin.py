from django.contrib import admin

from home.models import Book, PendingRequest, RequestTicket

admin.site.register(Book)
admin.site.register(PendingRequest)
admin.site.register(RequestTicket)
