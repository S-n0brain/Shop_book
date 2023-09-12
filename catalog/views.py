from django.shortcuts import render
from .models import Book, BookInstance, Author, Genre
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin


def index(request):
    """Генерация некоторых клавных объектов"""
    num_books = Book.objects.all().count()
    num_instance = BookInstance.objects.all().count()
    # Доступные книги (на складе)
    num_instances_available = BookInstance.objects.filter(status__name__exact='На складе').count()
    # Авторы книг
    num_authors = Author.objects.all().count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    req = request.get_full_path()
    print(f'full path: {req}')

    return render(request=request, template_name='index.html',
                  context={'num_books': num_books,
                           'num_instance': num_instance,
                           'num_instances_available': num_instances_available,
                           'num_authors': num_authors,
                           'num_visits': num_visits})


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
        context = ListView.get_context_data(self, **kwargs)
        print(context)
        return context


class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    model = BookInstance
    template_name = 'bookinstance_list_borrowed_user.html'
    paginate_by = 5

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__name='В заказе').order_by(
            'due_back')
