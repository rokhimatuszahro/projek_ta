from django.contrib import admin
from django.urls import path
from analisis_sentimen.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', dashboard, name='dashboard'),
    # path('upload/', upload, name='upload'),
]
