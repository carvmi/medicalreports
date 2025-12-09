from django.contrib import admin
from django.urls import include, path
from institution import views
# from users import views
# from reports import views



urlpatterns = [
    path("institution/", views.institution),
    path("patients/", include("patients.urls")),
    path("admin/", admin.site.urls),
]