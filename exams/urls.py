from django.urls import include, path
from exams.views import eview, ecreate, eedit, edelete, exam_report_pdf

urlpatterns = [
    path("add", ecreate, name='exams.ecreate'),
    path("", eview, name='exams.eview'),
    path("edit/<int:id>", eedit, name='exams.eedit'),
    path("delete/<int:id>", edelete, name='exams.edelete'),
    path("report/<int:id>", exam_report_pdf, name="exams.report"),
]
