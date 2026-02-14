from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from apps.institution.forms import AddressForm, InstForm
from apps.institution.models import Address, Institution

from .common import build_file_url, get_request_data, json_error, require_auth, soft_delete


def address_to_dict(address):
    if not address:
        return None
    return {
        "id": address.id,
        "rua": address.rua,
        "cep": address.cep,
        "bairro": address.bairro,
        "cidade": address.cidade,
        "uf": address.uf,
        "number": address.number,
        "is_active": address.is_active,
    }


def institution_to_dict(request, institution):
    return {
        "id": institution.id,
        "name": institution.name,
        "endereco_fisico_id": institution.endereco_fisico_id,
        "endereco_fisico": address_to_dict(institution.endereco_fisico),
        "site": institution.site,
        "phone": institution.phone,
        "email": institution.email,
        "itype": institution.itype,
        "logo_url": build_file_url(request, institution.logo),
        "is_active": institution.is_active,
    }


@csrf_exempt
def addresses_api(request, id=None):
    auth_error = require_auth(request)
    if auth_error:
        return auth_error

    if request.method == "GET":
        if id is None:
            addresses = Address.objects.all()
            return JsonResponse({"data": [address_to_dict(a) for a in addresses]}, status=200)
        address = get_object_or_404(Address, pk=id)
        return JsonResponse({"data": address_to_dict(address)}, status=200)

    if request.method in {"POST", "PUT", "PATCH"}:
        data, error = get_request_data(request)
        if error:
            return error
        if id is None and request.method != "POST":
            return json_error("ID obrigatorio para atualizar.", status=400)
        instance = get_object_or_404(Address, pk=id, is_active=True) if id else None
        form = AddressForm(data, instance=instance)
        if form.is_valid():
            address = form.save()
            status_code = 201 if instance is None else 200
            return JsonResponse({"data": address_to_dict(address)}, status=status_code)
        return json_error("Erro de validacao.", status=400, details=form.errors)

    if request.method == "DELETE":
        if id is None:
            return json_error("ID obrigatorio para excluir.", status=400)
        address = get_object_or_404(Address, pk=id, is_active=True)
        soft_delete(address)
        return JsonResponse({"data": {"deleted": True}}, status=200)

    return json_error("Metodo nao permitido.", status=405)


@csrf_exempt
def institutions_api(request, id=None):
    auth_error = require_auth(request)
    if auth_error:
        return auth_error

    if request.method == "GET":
        if id is None:
            institutions = Institution.objects.all()
            return JsonResponse(
                {"data": [institution_to_dict(request, inst) for inst in institutions]},
                status=200,
            )
        institution = get_object_or_404(Institution, pk=id)
        return JsonResponse({"data": institution_to_dict(request, institution)}, status=200)

    if request.method in {"POST", "PUT", "PATCH"}:
        data, error = get_request_data(request)
        if error:
            return error
        if id is None and request.method != "POST":
            return json_error("ID obrigatorio para atualizar.", status=400)
        instance = get_object_or_404(Institution, pk=id, is_active=True) if id else None
        form = InstForm(data, request.FILES, instance=instance)
        if form.is_valid():
            institution = form.save()
            status_code = 201 if instance is None else 200
            return JsonResponse({"data": institution_to_dict(request, institution)}, status=status_code)
        return json_error("Erro de validacao.", status=400, details=form.errors)

    if request.method == "DELETE":
        if id is None:
            return json_error("ID obrigatorio para excluir.", status=400)
        institution = get_object_or_404(Institution, pk=id, is_active=True)
        soft_delete(institution)
        return JsonResponse({"data": {"deleted": True}}, status=200)

    return json_error("Metodo nao permitido.", status=405)
