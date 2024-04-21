from django.contrib import admin
from .models import Book, BorrowedBook, Author

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(BorrowedBook)
