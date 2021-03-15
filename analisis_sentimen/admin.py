from django.contrib import admin
from .models import *

@admin.register(Datasets)
class DatasetsAdmin(admin.ModelAdmin):
    exclude = ('tweet', 'tanggal_update')
