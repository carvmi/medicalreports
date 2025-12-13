from django.urls import include, path
from medprofiles import views

urlpatterns = [
    path("criar/", views.add),
    path("store/", views.store),
]