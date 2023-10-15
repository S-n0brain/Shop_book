from django.urls import path
from catalog import views

app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('authors_add/', views.authors_add, name='authors-add'),
    path('create_author/', views.create_author, name='create'),
    path('delete_author/<int:pk>/', views.delete_author, name='delete'),
    path('edit_author/<int:pk>/', views.edit_author, name='edit'),
    path('book_create/', views.BookCreateView.as_view(), name='book_create'),
    path('book_update/<int:pk>', views.BookUpdateView.as_view(), name='book_update'),
    path('book_delete/<int:pk>', views.BookDeleteView.as_view(), name='book_delete')
]