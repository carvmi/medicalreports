from django.contrib import admin
from medprofiles import models
# Register your models here.

@admin.register(models.HealthProfessional)
class MedprofilesAdmin(admin.ModelAdmin):
  ...