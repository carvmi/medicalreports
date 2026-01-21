from django.urls import include, path
from exams.views import view, create, edit, delete

urlpatterns = [
    path("add", create, name='exams.create'),
    path("", view, name='exams.view'),
    path("edit/<int:id>", edit, name='exams.edit'),
    path("delete/<int:id>", delete, name='exams.delete'),]