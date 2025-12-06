from django.contrib import admin
from institution import models
# Register your models here.

@admin.register(models.Institution)
class InstitutionAdmin(admin.ModelAdmin):
  list_display = 'id', 'name', 'itype', 'phone', 'email',
  ordering = 'id',
  search_fields = 'id', 'name', 'itype',
  list_per_page = 10 
  list_max_show_all = 50 
  list_filter = 'itype',