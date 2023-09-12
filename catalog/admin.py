from django.contrib import admin
from catalog.models import *


class BookInstanceInline(admin.TabularInline):
    model = BookInstance


class BookInline(admin.StackedInline):
    model = Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'language', 'display_author')
    list_filter = ('genre', 'author')
    list_display_links = ['title', 'language', 'display_author']
    inlines = [BookInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ['book', 'status', 'due_back',  'borrower']
    list_filter = ['book', 'status',  'borrower']
    fieldsets = [['Экземпляр книги',
                  {
                      'fields': [('book', 'imprint'), 'inv_nom']
                  }],
                 [
                     'Статус и окончание его действия',
                     {
                         'fields': ['status', 'due_back',  'borrower']
                     }
                 ]]


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    inlines = [BookInline]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    inlines = [BookInline]


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    inlines = [BookInstanceInline]
