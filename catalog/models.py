from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date


class Genre(models.Model):
    """Жанры книг"""
    name = models.CharField(max_length=200, help_text='Введите жанр книги',
                            verbose_name='Жанр книги')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Language(models.Model):
    """Языки книг"""
    name = models.CharField(max_length=20, help_text='Введите язык книги',
                            verbose_name='Язык книги')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Язык'
        verbose_name_plural = 'Языки'


class Author(models.Model):
    """Авторы книг"""
    first_name = models.CharField(max_length=100, help_text='Введите имя автора',
                                  verbose_name='Имя автора')
    last_name = models.CharField(max_length=100, help_text='Введите фамилию автора',
                                 verbose_name='Фамилия автора')
    date_of_birth = models.DateField(help_text='Введите дату рождения', verbose_name='Дата рождения',
                                     null=True, blank=True)
    date_of_death = models.DateField(help_text='Введите дату смерти', verbose_name='Дата смерти',
                                     null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['-id']

class Book(models.Model):
    """Книги"""
    title = models.CharField(max_length=200,
                             help_text='Введите назваие книги',
                             verbose_name='Название книги')
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE,
                              help_text=" Выберите жанр для книги",
                              verbose_name="Жaнp книги", null=True)
    language = models.ForeignKey('Language', on_delete=models.CASCADE,
                                 help_text=" Выберите язык для книги",
                                 verbose_name="Язык книги", null=True)
    author = models.ManyToManyField('Author',
                                    help_text="Выберите автора книги",
                                    verbose_name="Aвтop книги")
    summary = models.TextField(help_text="Введите краткое описание книги",
                               verbose_name="Аннотация книги")
    isbn = models.CharField(max_length=13,
                            help_text="Должно содержать 13 символов",
                            verbose_name="ISBN книги")

    def __str__(self):
        return self.title

    def display_author(self):
        authors = [author.last_name for author in self.author.all()]
        return ', '.join(authors)

    display_author.short_description = 'Авторы'

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def get_absolute_url(self):
        """Возвращает URL-aдpec для доступа к определенному экземпляру книги"""
        return reverse('catalog:book-detail', kwargs={'pk': str(self.id)})


class Status(models.Model):
    """Статус книги"""
    name = models.CharField(max_length=20, help_text="Введите статус экземпляра книги",
                            verbose_name='Статус экземпляра книги')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class BookInstance(models.Model):
    """Экземпляры книг"""
    book = models.ForeignKey('Book', on_delete=models.CASCADE, null=True)
    inv_nom = models.CharField(max_length=20, null=True,
                               help_text="Введите инвентарный номер экземпляра",
                               verbose_name="Инвентарный номер")
    imprint = models.CharField(max_length=200,
                               help_text="Введите издательство и год выnуска",
                               verbose_name="Издательство")
    status = models.ForeignKey('Status', on_delete=models.CASCADE, null=True,
                               help_text='Изменить состояние экземпляра',
                               verbose_name="Cтaтyc экземпляра книги")
    due_back = models.DateField(null=True, blank=True, help_text="Введите конец срока статуса",
                                verbose_name="Дaтa окончания статуса")
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL,
                                 null=True, blank=True, verbose_name='Заказчик',
                                 help_text='Выберите заказчика книги')

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    class Meta:
        ordering = ['due_back']
        verbose_name = 'Экземпляр книги'
        verbose_name_plural = 'Экземпляры книг'

    def __str__(self):
        return f'{self.inv_nom} {self.book} {self.status}'
