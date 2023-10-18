from django import forms
from datetime import date
from django.forms import ModelForm
from .models import *


class AuthorsForm(forms.Form):
    first_name = forms.CharField(label='Имя автора')
    last_name = forms.CharField(label='Фамилия')
    date_of_birth = forms.DateField(initial=format(date.today()), widget=forms.widgets.DateInput(attrs={'type': date}))
    date_of_death = forms.DateField(initial=format(date.today()), widget=forms.widgets.DateInput(attrs={'type': date}))


class BookForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = '''form-control border border-warning
                                                    border-2'''
        self.fields["title"].widget.attrs.update({"class": " form-control border border-2 border-danger"})

    class Meta:
        model = Book
        fields = '__all__'


class GenreForm(ModelForm):
    def __init__(self, *args, **kwargs):
        ModelForm.__init__(self, *args, **kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': 'Введите жанр книги', 'class': 'form-control '})
    class Meta:
        model = Genre
        fields = '__all__'
