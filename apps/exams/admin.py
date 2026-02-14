from django.contrib import admin

from . import models

@admin.register(models.MammogramExam)
class ExamsAdmin(admin.ModelAdmin):
    ...
