from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publication_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'


class BorrowedBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(User, on_delete=models.CASCADE)
    due_date = models.DateField()
    returned = models.BooleanField(default=False)

    def __str__(self):
        return self.book + ' - ' + self.borrower + ' - ' + self.due_date

    class Meta:
        verbose_name = 'Borrowed Book'
        verbose_name_plural = 'Borrowed Books'
