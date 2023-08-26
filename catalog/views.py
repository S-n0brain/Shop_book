from django.shortcuts import render
from .models import Book, BookInstance, Author, Genre
from django.views.generic import ListView, DetailView


def index(request):
    """Генерация некоторых клавных объектов"""
    num_books = Book.objects.all().count()
    num_instance = BookInstance.objects.all().count()
    # Доступные книги (на складе)
    num_instances_available = BookInstance.objects.filter(status__name__exact='На складе').count()
    # Авторы книг
    num_authors = Author.objects.all().count()
    req = request.get_full_path()
    print(req)
    return render(request=request, template_name='index.html',
                  context={'num_books': num_books,
                           'num_instance': num_instance,
                           'num_instances_available': num_instances_available,
                           'num_authors': num_authors})


class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'
    paginate_by = 3


class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'


class AuthorListView(ListView):
    model = Author
    template_name = 'author_list.html'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        print(self.request.get_full_path())
        context = super().get_context_data(**kwargs)
        print(context)
        return context
