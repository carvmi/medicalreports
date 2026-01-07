from django.urls import include, path
from institution.views import view, create, edit, delete

urlpatterns = [
    path("add", create, name='inst.create'),
    path("", view, name='inst.view'),
    path("edit/<int:id>", edit, name='inst.edit'),
    path("delete/<int:id>", delete, name='inst.delete'),
]