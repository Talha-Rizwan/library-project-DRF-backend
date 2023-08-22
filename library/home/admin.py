from django.contrib import admin

from home.models import Book, PendingRequest

admin.site.register(Book)
admin.site.register(PendingRequest)
