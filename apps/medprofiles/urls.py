from django.urls import path
from .views import view, create, edit, delete

urlpatterns = [
    path("add", create, name='med.create'),
    path("", view, name='med.view'),
    path("edit/<int:id>", edit, name='med.edit'),
    path("delete/<int:id>", delete, name='med.delete'),
]
