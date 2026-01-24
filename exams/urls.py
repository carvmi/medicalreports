from django.urls import include, path
from exams.views import eview, ecreate, eedit, edelete

urlpatterns = [
    path("add", ecreate, name='exams.ecreate'),
    path("", eview, name='exams.eview'),
    path("edit/<int:id>", eedit, name='exams.eedit'),
    path("delete/<int:id>", edelete, name='exams.edelete'),]