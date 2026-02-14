from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api/", include("apps.api.urls")),
    path("institution/", include("apps.institution.urls")),
    path("patients/", include("apps.patients.urls")),
    path("medprofiles/", include("apps.medprofiles.urls")),
    path("", include("apps.login.urls")),
    path("exams/", include("apps.exams.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
