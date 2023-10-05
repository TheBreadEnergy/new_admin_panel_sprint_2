from django.contrib import admin
from django.urls import path

from docker_compose.movies_admin import movies

urlpatterns = [
    path('admin/', admin.site.urls),
]
