from django.contrib import admin
from django.urls import include, path
from institution import views

urlpatterns = [
    path("institution/", views.institution),
    path("patients/", include("patients.urls")),
    path("medprofiles/", include("medprofiles.urls")),
    path("admin/", admin.site.urls),
]