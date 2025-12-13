from django.contrib import admin
from medprofiles import models
# Register your models here.

@admin.register(models.Medprofile)
class MedprofileAdmin(admin.ModelAdmin):
  ...