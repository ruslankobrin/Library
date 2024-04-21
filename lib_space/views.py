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

        if author and title:
            books = Book.objects.filter(author__name__icontains=author, title__icontains=title)
        elif author:
            books = Book.objects.filter(author__name__icontains=author)
        elif title:
            books = Book.objects.filter(title__icontains=title)
        else:
            books = []

        return render(request, 'search_books.html', {'books': books})


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