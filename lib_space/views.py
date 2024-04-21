from django.shortcuts import render
from .models import Book, BorrowedBook


def search_books(request):
    if request.method == 'GET':
        author = request.GET.get('author')
        title = request.GET.get('title')

        if author and title:
            books = Book.objects.filter(author__name__icontains=author, title__icontains=title)
        elif author:
            books = Book.objects.filter(author__name__icontains=author)
        elif title:
            books = Book.objects.filter(title__icontains=title)
        else:
            books = []

        return render(request, 'search_books.html', {'books': books})
