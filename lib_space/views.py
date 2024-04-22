from datetime import date, timedelta

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Book, BorrowedBook


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/lib_space/search')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def search_books(request):
    if request.method == 'GET':
        author = request.GET.get('author')
        title = request.GET.get('title')
        borrower = request.GET.get('borrower')

        borrowed_books = BorrowedBook.objects.select_related("borrower")
        if author:
            borrowed_books = borrowed_books.filter(book__author__name__icontains=author)
        if title:
            borrowed_books = borrowed_books.filter(book__title__icontains=title)
        if borrower:
            borrowed_books = borrowed_books.filter(borrower__username__icontains=borrower)

        books_with_borrowers = [{'title': borrowed_book.book.title, 'author': borrowed_book.book.author,
                                 'borrower': borrowed_book.borrower.username} for borrowed_book in borrowed_books]

        return render(request, 'search_books.html', {'books_with_borrowers': books_with_borrowers})


def borrow_books(request):
    if request.method == 'POST':
        book_id = request.POST.get('book')
        due_date = request.POST.get('due_date')

        if not (book_id and due_date):
            messages.error(request, 'Please select a book and enter a due date.')
            return redirect('borrow_books')

        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            messages.error(request, 'Selected book does not exist.')
            return redirect('borrow_books')

        borrowed_book = BorrowedBook(book=book, borrower=request.user, due_date=due_date)
        borrowed_book.save()

        messages.success(request, 'You have borrowed ' + book.title + ' by ' + book.author.name + '.')
        return redirect('borrow_books')

    else:
        books = Book.objects.all()
        return render(request, 'borrow_books.html', {'books': books})


def manage_borrowed_books(request):
    current_date = date.today()
    borrowed_books = BorrowedBook.objects.all()

    overdue_books = []
    due_soon_books = []
    normal_books = []

    for book in borrowed_books:
        if not book.returned:
            if book.due_date < current_date:
                overdue_books.append(book)
            elif current_date < book.due_date <= current_date + timedelta(days=7):
                due_soon_books.append(book)
            else:
                normal_books.append(book)

    return render(
        request,
        'manage_borrowed_books.html',
        {
            'overdue_books': overdue_books,
            'due_soon_books': due_soon_books,
            'normal_books': normal_books,
            'current_date': current_date
        }
    )
