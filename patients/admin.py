from django.contrib import admin
from patients import models
# Register your models here.

@admin.register(models.Patient)
class PatientAdmin(admin.ModelAdmin):
  list_display = 'id', 'full_name', 'cpf',
  ordering = 'id',
  search_fields = 'id', 'full_name', 'cpf',
  list_per_page = 10 
  list_max_show_all = 50 
  list_filter = 'sex',