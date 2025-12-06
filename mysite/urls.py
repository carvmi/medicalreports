from django.contrib import admin
from django.urls import include, path
from institution import views
# from patients import views
# from users import views
# from reports import views



urlpatterns = [
    path("institution/", views.institution),
    # path("patients/", include("patients.urls")),
    # path("users/", include("users.urls")),
    # path("reports/", include("reports.urls")),
    path("admin/", admin.site.urls),
]