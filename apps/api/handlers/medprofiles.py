from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from apps.medprofiles.forms import MedForm
from apps.medprofiles.models import HealthProfessional

from .common import get_request_data, json_error, require_auth, soft_delete


def professional_to_dict(professional):
    return {
        "id": professional.id,
        "full_name": professional.full_name,
        "position": professional.position,
        "specialization": professional.specialization,
        "professional_registration": professional.professional_registration,
        "institutions": [
            {"id": inst.id, "name": inst.name} for inst in professional.institution.all()
        ],
        "is_active": professional.is_active,
    }


@csrf_exempt
def medprofiles_api(request, id=None):
    auth_error = require_auth(request)
    if auth_error:
        return auth_error

    if request.method == "GET":
        if id is None:
            professionals = HealthProfessional.objects.all()
            return JsonResponse(
                {"data": [professional_to_dict(p) for p in professionals]}, status=200
            )
        professional = get_object_or_404(HealthProfessional, pk=id)
        return JsonResponse({"data": professional_to_dict(professional)}, status=200)

    if request.method in {"POST", "PUT", "PATCH"}:
        data, error = get_request_data(request)
        if error:
            return error
        if id is None and request.method != "POST":
            return json_error("ID obrigatorio para atualizar.", status=400)
        instance = get_object_or_404(HealthProfessional, pk=id, is_active=True) if id else None
        form = MedForm(data, instance=instance)
        if form.is_valid():
            professional = form.save()
            status_code = 201 if instance is None else 200
            return JsonResponse({"data": professional_to_dict(professional)}, status=status_code)
        return json_error("Erro de validacao.", status=400, details=form.errors)

    if request.method == "DELETE":
        if id is None:
            return json_error("ID obrigatorio para excluir.", status=400)
        professional = get_object_or_404(HealthProfessional, pk=id, is_active=True)
        soft_delete(professional)
        return JsonResponse({"data": {"deleted": True}}, status=200)

    return json_error("Metodo nao permitido.", status=405)
