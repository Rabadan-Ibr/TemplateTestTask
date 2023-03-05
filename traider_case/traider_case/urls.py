from django.contrib import admin
from django.urls import path, re_path

from menu.views import index, not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('404/', not_found),
    path('institutions/schools/', index, name='schools'),
    path('institutions/universities/faculties/', index, name='faculties'),
    re_path(r'.*', index),
]
