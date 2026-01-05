from django.urls import include, path
from patients.views import plist, pform

urlpatterns = [
    path("add", pform, name='pform'),
    path("", plist, name='plist'),
]