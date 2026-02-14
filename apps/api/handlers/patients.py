from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from apps.patients.forms import PatientForm
from apps.patients.models import Patient

from .common import as_date, as_datetime, get_request_data, json_error, require_auth, soft_delete


def patient_to_dict(patient):
    return {
        "id": patient.id,
        "full_name": patient.full_name,
        "birth_date": as_date(patient.birth_date),
        "gender": patient.gender,
        "cpf": patient.cpf,
        "phone": patient.phone,
        "email": patient.email,
        "allergies": patient.allergies,
        "pre_existing_conditions": patient.pre_existing_conditions,
        "notes": patient.notes,
        "created_at": as_datetime(patient.created_at),
        "updated_at": as_datetime(patient.updated_at),
        "is_active": patient.is_active,
    }


@csrf_exempt
def patients_api(request, id=None):
    auth_error = require_auth(request)
    if auth_error:
        return auth_error

    if request.method == "GET":
        if id is None:
            patients = Patient.objects.all()
            return JsonResponse({"data": [patient_to_dict(p) for p in patients]}, status=200)
        patient = get_object_or_404(Patient, pk=id)
        return JsonResponse({"data": patient_to_dict(patient)}, status=200)

    if request.method in {"POST", "PUT", "PATCH"}:
        data, error = get_request_data(request)
        if error:
            return error
        if id is None and request.method != "POST":
            return json_error("ID obrigatorio para atualizar.", status=400)
        instance = get_object_or_404(Patient, pk=id, is_active=True) if id else None
        form = PatientForm(data, instance=instance)
        if form.is_valid():
            patient = form.save()
            status_code = 201 if instance is None else 200
            return JsonResponse({"data": patient_to_dict(patient)}, status=status_code)
        return json_error("Erro de validacao.", status=400, details=form.errors)

    if request.method == "DELETE":
        if id is None:
            return json_error("ID obrigatorio para excluir.", status=400)
        patient = get_object_or_404(Patient, pk=id, is_active=True)
        soft_delete(patient)
        return JsonResponse({"data": {"deleted": True}}, status=200)

    return json_error("Metodo nao permitido.", status=405)
