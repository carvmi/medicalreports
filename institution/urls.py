from django.urls import include, path
from institution.views import view, create, edit, delete, adcreate

urlpatterns = [
    path("add", create, name='inst.create'),
    path("", view, name='inst.view'),
    path("edit/<int:id>", edit, name='inst.edit'),
    path("address/create", adcreate, name='inst.adcreate'),
    path("delete/<int:id>", delete, name='inst.delete'),
]