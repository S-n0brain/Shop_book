# Generated by Django 4.2.4 on 2023-08-18 18:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_alter_book_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='language',
            field=models.ForeignKey(help_text=' Выберите язык для книги', null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.language', verbose_name='Язык книги'),
        ),
    ]
