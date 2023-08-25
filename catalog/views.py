from django.shortcuts import render
from .models import Book, BookInstance, Author, Genre


def index(request):
    """Генерация некоторых клавных объектов"""
    num_books = Book.objects.all().count()
    num_instance = BookInstance.objects.all().count()
    #Доступные книги (на складе)
    num_instances_available = BookInstance.objects.filter(status__bookinstance__exact=2).count()
    #Авторы книг
    num_authors = Author.objects.all().count()
    return render(request=request, template_name='index.html',
                  context={'num_books': num_books,
                           'num_instance': num_instance,
                           'num_instances_available': num_instances_available,
                           'num_authors': num_authors})
