from django.contrib import admin
from exams import models

@admin.register(models.MammogramExam)
class ExamsAdmin(admin.ModelAdmin):
    ...
