from django.contrib import admin
from catalog.models import *

admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Book)
admin.site.register(Status)
admin.site.register(BookInstance)

