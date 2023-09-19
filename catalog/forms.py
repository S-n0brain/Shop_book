from django import forms
from datetime import date


class AuthorsForm(forms.Form):
    first_name = forms.CharField(label='Имя автора')
    last_name = forms.CharField(label='Фамилия')
    date_of_birth = forms.DateField(initial=format(date.today()), widget=forms.widgets.DateInput(attrs={'type': date}))
    date_of_death = forms.DateField(initial=format(date.today()), widget=forms.widgets.DateInput(attrs={'type': date}))
