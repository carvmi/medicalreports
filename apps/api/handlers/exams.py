from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from apps.exams.forms import MammogramExamForm
from apps.exams.models import MammogramExam

from .common import (
    as_date,
    as_datetime,
    build_file_url,
    get_client_ip,
    get_request_data,
    json_error,
    require_auth,
    soft_delete,
)


def exam_to_dict(request, exam):
    return {
        "id": exam.id,
        "patient_id": exam.patient_id,
        "patient_name": exam.patient.full_name if exam.patient_id else None,
        "local_id": exam.local_id,
        "local_name": exam.local.name if exam.local_id else None,
        "exam_date": as_date(exam.exam_date),
        "description": exam.description,
        "result": exam.result,
        "itype": exam.itype,
        "acceptance_term": exam.acceptance_term,
        "user_ip": exam.user_ip,
        "created_at": as_datetime(exam.created_at),
        "image_url": build_file_url(request, exam.image),
        "is_active": exam.is_active,
    }


@csrf_exempt
def exams_api(request, id=None):
    auth_error = require_auth(request)
    if auth_error:
        return auth_error

    if request.method == "GET":
        if id is None:
            exams = MammogramExam.objects.all()
            return JsonResponse({"data": [exam_to_dict(request, e) for e in exams]}, status=200)
        exam = get_object_or_404(MammogramExam, pk=id)
        return JsonResponse({"data": exam_to_dict(request, exam)}, status=200)

    if request.method in {"POST", "PUT", "PATCH"}:
        data, error = get_request_data(request)
        if error:
            return error
        if id is None and request.method != "POST":
            return json_error("ID obrigatorio para atualizar.", status=400)
        instance = get_object_or_404(MammogramExam, pk=id, is_active=True) if id else None
        form = MammogramExamForm(data, request.FILES, instance=instance)
        if form.is_valid():
            exam = form.save(commit=False)
            if instance is None:
                exam.user_ip = get_client_ip(request)
            exam.save()
            form.save_m2m()
            status_code = 201 if instance is None else 200
            return JsonResponse({"data": exam_to_dict(request, exam)}, status=status_code)
        return json_error("Erro de validacao.", status=400, details=form.errors)

    if request.method == "DELETE":
        if id is None:
            return json_error("ID obrigatorio para excluir.", status=400)
        exam = get_object_or_404(MammogramExam, pk=id, is_active=True)
        soft_delete(exam)
        return JsonResponse({"data": {"deleted": True}}, status=200)

    return json_error("Metodo nao permitido.", status=405)
