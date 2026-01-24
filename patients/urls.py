from django.urls import include, path
from patients.views import pview, pcreate, pedit, pdelete

urlpatterns = [
    path("add", pcreate, name='p.create'),
    path("", pview, name='p.view'),
    path("edit/<int:id>", pedit, name='p.edit'),
    path("delete/<int:id>", pdelete, name='p.delete'),
]