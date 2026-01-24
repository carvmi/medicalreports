from django.urls import include, path
from institution.views import iview, icreate, iedit, idelete, adcreate

urlpatterns = [
    path("add", icreate, name='inst.icreate'),
    path("", iview, name='inst.iview'),
    path("edit/<int:id>", iedit, name='inst.iedit'),
    path("address/create", adcreate, name='inst.adcreate'),
    path("delete/<int:id>", idelete, name='inst.idelete'),
]