from django.urls import path
from api import views

urlpatterns = [
    path("docs", views.docs_api, name="api.docs"),
    path("auth/register", views.register_api, name="api.register"),
    path("auth/login", views.login_api, name="api.login"),
    path("auth/me", views.me_api, name="api.me"),
    path("patients/", views.patients_api, name="api.patients"),
    path("patients/<int:id>/", views.patients_api, name="api.patients.detail"),
    path("institutions/", views.institutions_api, name="api.institutions"),
    path("institutions/<int:id>/", views.institutions_api, name="api.institutions.detail"),
    path("addresses/", views.addresses_api, name="api.addresses"),
    path("addresses/<int:id>/", views.addresses_api, name="api.addresses.detail"),
    path("medprofiles/", views.medprofiles_api, name="api.medprofiles"),
    path("medprofiles/<int:id>/", views.medprofiles_api, name="api.medprofiles.detail"),
    path("exams/", views.exams_api, name="api.exams"),
    path("exams/<int:id>/", views.exams_api, name="api.exams.detail"),
]
