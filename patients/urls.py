from django.urls import include, path
from patients.views import view, create, edit, delete

urlpatterns = [
    path("add", create, name='p.create'),
    path("", view, name='p.view'),
    path("edit/<int:id>", edit, name='p.edit'),
    path("delete/<int:id>", delete, name='p.delete'),
]