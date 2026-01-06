from django.urls import include, path
from medprofiles.views import view, create, edit, delete

urlpatterns = [
    path("add", create, name='create'),
    path("", view, name='view'),
    path("edit/<int:id>", edit, name='edit'),
    path("delete/<int:id>", delete, name='delete'),
]