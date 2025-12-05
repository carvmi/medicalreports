from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("institution/", include("institution.urls")),
    path("patients/", include("patients.urls")),
    path("users/", include("users.urls")),
    path("reports/", include("reports.urls")),
    path("admin/", admin.site.urls),
]