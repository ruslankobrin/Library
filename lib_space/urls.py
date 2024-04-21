from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'search/', views.search_books, name='search_books'),
    url('borrow/', views.borrow_books, name='borrow_books'),
]
