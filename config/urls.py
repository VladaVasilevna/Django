from django.contrib import admin
from django.urls import path, include
from catalog.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('home/', include('catalog.urls', namespace='catalog')),
]
