from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("institution/", include("institution.urls")),
    path("admin/", admin.site.urls),
]