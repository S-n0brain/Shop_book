from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from .models import Book, BookInstance, Author, Genre
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import BookForm


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


def authors_add(request):
    authors = Author.objects.all()
    pagin_authors = Paginator(authors, per_page=3)
    page_number = request.GET.get('page')
    page_obj = pagin_authors.get_page(page_number)
    return render(request, template_name='authors_add.html',
                  context={"authors": authors, 'page_object': page_obj})


def create_author(request):
    if request.method == 'POST':
        author = Author()
        author.first_name = request.POST.get('first_name')
        author.last_name = request.POST.get('last_name')
        author.date_of_birth = request.POST.get('date_of_birth')
        author.date_of_death = request.POST.get('date_of_death')
        if author.date_of_death == '':
            author.date_of_death = None
        if author.date_of_birth > author.date_of_death:
            return redirect('catalog:authors-add')
        else:
            author.save()
            return redirect('catalog:authors-add')


def delete_author(request, pk):
    try:
        author = Author.objects.get(pk=pk)
    except Author.DoesNotExist:
        return HttpResponseNotFound("""<script>
                alert('Такого id автора не существует!')
                </script>""")
    else:
        author.delete()
        return redirect('catalog:authors-add')


def edit_author(request, pk):
    author = Author.objects.get(pk=pk)
    if request.method == 'POST':
        author.first_name = request.POST.get('first_name')
        author.last_name = request.POST.get('last_name')
        author.date_of_birth = request.POST.get('date_of_birth')
        author.date_of_death = request.POST.get('date_of_death')
        if author.date_of_death == '':
            author.date_of_death = None
        if author.date_of_birth > author.date_of_death:
            return redirect('catalog:edit', pk=author.pk)
        else:
            author.save()
            return redirect('catalog:authors-add')
    else:
        return render(request, template_name='edit_author.html', context={'author': author})


class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy('catalog:books')
    template_name = 'book_form.html'


class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'book_form.html'
    success_url = reverse_lazy('catalog:books')


class BookDeleteView(DeleteView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy('catalog:books')
    template_name = 'book_confirm_delete.html'

