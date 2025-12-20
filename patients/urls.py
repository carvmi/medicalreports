from django.urls import include, path
from patients import views

urlpatterns = [
    path("add", views.pform),
]