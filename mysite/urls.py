from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("institution/", include("institution.urls")),
    path("patients/", include("patients.urls")),
    path("medprofiles/", include("medprofiles.urls")),
    path("", include("login.urls")),
    path("exams/", include("exams.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
