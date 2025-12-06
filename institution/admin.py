from django.contrib import admin
from institution import models
# Register your models here.

@admin.register(models.Institution)
class InstitutionAdmin(admin.ModelAdmin):
  ...