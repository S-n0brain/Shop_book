from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls')),
    path('users/', include('users.urls')),
    path('', include('django.contrib.auth.urls')),
]
