from django.contrib import admin
from django.urls import path, include
from catalog import views
from django.conf.urls import handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls')),
    path('users/', include('users.urls')),
    path('', include('django.contrib.auth.urls')),
]

handler404 = 'catalog.views.error_404'