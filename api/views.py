import json

from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.http import JsonResponse, QueryDict
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from exams.forms import MammogramExamForm
from exams.models import MammogramExam
from institution.forms import InstForm, AddressForm
from institution.models import Institution, Address
from medprofiles.forms import MedForm
from medprofiles.models import HealthProfessional
from patients.forms import PatientForm
from patients.models import Patient


def _json_error(message, status=400, details=None):
    payload = {"error": message}
    if details is not None:
        payload["details"] = details
    return JsonResponse(payload, status=status)


def _require_auth(request):
    if not request.user.is_authenticated:
        return _json_error("Autenticacao necessaria.", status=401)
    return None


def _parse_json_body(request):
    raw = request.body.decode("utf-8") if request.body else ""
    if not raw:
        return {}, None
    try:
        return json.loads(raw), None
    except json.JSONDecodeError:
        return None, _json_error("JSON invalido.", status=400)


def _get_request_data(request):
    content_type = request.content_type or ""
    if "application/json" in content_type:
        data, error = _parse_json_body(request)
        if error:
            return None, error
        qd = QueryDict(mutable=True)
        for key, value in (data or {}).items():
            if isinstance(value, list):
                qd.setlist(key, [str(item) for item in value])
            elif value is None:
                qd[key] = ""
            else:
                qd[key] = str(value)
        return qd, None
    return request.POST, None


def _date(value):
    return value.isoformat() if value else None


def _datetime(value):
    return value.isoformat() if value else None


def _build_file_url(request, file_field):
    if not file_field:
        return None
    try:
        return request.build_absolute_uri(file_field.url)
    except Exception:
        return None


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
        "logo_url": _build_file_url(request, institution.logo),
    }


def patient_to_dict(patient):
    return {
        "id": patient.id,
        "full_name": patient.full_name,
        "birth_date": _date(patient.birth_date),
        "gender": patient.gender,
        "cpf": patient.cpf,
        "phone": patient.phone,
        "email": patient.email,
        "allergies": patient.allergies,
        "pre_existing_conditions": patient.pre_existing_conditions,
        "notes": patient.notes,
        "created_at": _datetime(patient.created_at),
        "updated_at": _datetime(patient.updated_at),
    }


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
    }


def exam_to_dict(request, exam):
    return {
        "id": exam.id,
        "patient_id": exam.patient_id,
        "patient_name": exam.patient.full_name if exam.patient_id else None,
        "local_id": exam.local_id,
        "local_name": exam.local.name if exam.local_id else None,
        "exam_date": _date(exam.exam_date),
        "description": exam.description,
        "result": exam.result,
        "itype": exam.itype,
        "acceptance_term": exam.acceptance_term,
        "user_ip": exam.user_ip,
        "created_at": _datetime(exam.created_at),
        "image_url": _build_file_url(request, exam.image),
    }


def _get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    return request.META.get("REMOTE_ADDR")


def _soft_delete(instance):
    instance.is_active = False
    instance.deleted_at = timezone.now()
    instance.save(update_fields=["is_active", "deleted_at"])


@csrf_exempt
def register_api(request):
    if request.method != "POST":
        return _json_error("Metodo nao permitido.", status=405)
    data, error = _get_request_data(request)
    if error:
        return error
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not password:
        return _json_error("username e password sao obrigatorios.", status=400)

    if User.objects.filter(username=username).exists():
        return _json_error("Usuario ja existe.", status=400)

    user = User.objects.create_user(username=username, email=email, password=password)
    return JsonResponse(
        {"data": {"id": user.id, "username": user.username, "email": user.email}},
        status=201,
    )


@csrf_exempt
def login_api(request):
    if request.method != "POST":
        return _json_error("Metodo nao permitido.", status=405)
    data, error = _get_request_data(request)
    if error:
        return error
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return _json_error("username e password sao obrigatorios.", status=400)

    user = authenticate(request, username=username, password=password)
    if user is None:
        return _json_error("Usuario ou senha invalidos.", status=401)

    auth_login(request, user)
    return JsonResponse(
        {"data": {"id": user.id, "username": user.username, "email": user.email}},
        status=200,
    )


def me_api(request):
    auth_error = _require_auth(request)
    if auth_error:
        return auth_error
    user = request.user
    return JsonResponse(
        {"data": {"id": user.id, "username": user.username, "email": user.email}},
        status=200,
    )


@csrf_exempt
def patients_api(request, id=None):
    auth_error = _require_auth(request)
    if auth_error:
        return auth_error

    if request.method == "GET":
        if id is None:
            patients = Patient.objects.filter(is_active=True)
            return JsonResponse({"data": [patient_to_dict(p) for p in patients]}, status=200)
        patient = get_object_or_404(Patient, pk=id, is_active=True)
        return JsonResponse({"data": patient_to_dict(patient)}, status=200)

    if request.method in {"POST", "PUT", "PATCH"}:
        data, error = _get_request_data(request)
        if error:
            return error
        if id is None and request.method != "POST":
            return _json_error("ID obrigatorio para atualizar.", status=400)
        instance = get_object_or_404(Patient, pk=id, is_active=True) if id else None
        form = PatientForm(data, instance=instance)
        if form.is_valid():
            patient = form.save()
            status_code = 201 if instance is None else 200
            return JsonResponse({"data": patient_to_dict(patient)}, status=status_code)
        return _json_error("Erro de validacao.", status=400, details=form.errors)

    if request.method == "DELETE":
        if id is None:
            return _json_error("ID obrigatorio para excluir.", status=400)
        patient = get_object_or_404(Patient, pk=id, is_active=True)
        _soft_delete(patient)
        return JsonResponse({"data": {"deleted": True}}, status=200)

    return _json_error("Metodo nao permitido.", status=405)


@csrf_exempt
def addresses_api(request, id=None):
    auth_error = _require_auth(request)
    if auth_error:
        return auth_error

    if request.method == "GET":
        if id is None:
            addresses = Address.objects.filter(is_active=True)
            return JsonResponse({"data": [address_to_dict(a) for a in addresses]}, status=200)
        address = get_object_or_404(Address, pk=id, is_active=True)
        return JsonResponse({"data": address_to_dict(address)}, status=200)

    if request.method in {"POST", "PUT", "PATCH"}:
        data, error = _get_request_data(request)
        if error:
            return error
        if id is None and request.method != "POST":
            return _json_error("ID obrigatorio para atualizar.", status=400)
        instance = get_object_or_404(Address, pk=id, is_active=True) if id else None
        form = AddressForm(data, instance=instance)
        if form.is_valid():
            address = form.save()
            status_code = 201 if instance is None else 200
            return JsonResponse({"data": address_to_dict(address)}, status=status_code)
        return _json_error("Erro de validacao.", status=400, details=form.errors)

    if request.method == "DELETE":
        if id is None:
            return _json_error("ID obrigatorio para excluir.", status=400)
        address = get_object_or_404(Address, pk=id, is_active=True)
        _soft_delete(address)
        return JsonResponse({"data": {"deleted": True}}, status=200)

    return _json_error("Metodo nao permitido.", status=405)


@csrf_exempt
def institutions_api(request, id=None):
    auth_error = _require_auth(request)
    if auth_error:
        return auth_error

    if request.method == "GET":
        if id is None:
            institutions = Institution.objects.filter(is_active=True)
            return JsonResponse(
                {"data": [institution_to_dict(request, inst) for inst in institutions]},
                status=200,
            )
        institution = get_object_or_404(Institution, pk=id, is_active=True)
        return JsonResponse({"data": institution_to_dict(request, institution)}, status=200)

    if request.method in {"POST", "PUT", "PATCH"}:
        data, error = _get_request_data(request)
        if error:
            return error
        if id is None and request.method != "POST":
            return _json_error("ID obrigatorio para atualizar.", status=400)
        instance = get_object_or_404(Institution, pk=id, is_active=True) if id else None
        form = InstForm(data, request.FILES, instance=instance)
        if form.is_valid():
            institution = form.save()
            status_code = 201 if instance is None else 200
            return JsonResponse({"data": institution_to_dict(request, institution)}, status=status_code)
        return _json_error("Erro de validacao.", status=400, details=form.errors)

    if request.method == "DELETE":
        if id is None:
            return _json_error("ID obrigatorio para excluir.", status=400)
        institution = get_object_or_404(Institution, pk=id, is_active=True)
        _soft_delete(institution)
        return JsonResponse({"data": {"deleted": True}}, status=200)

    return _json_error("Metodo nao permitido.", status=405)


@csrf_exempt
def medprofiles_api(request, id=None):
    auth_error = _require_auth(request)
    if auth_error:
        return auth_error

    if request.method == "GET":
        if id is None:
            professionals = HealthProfessional.objects.filter(is_active=True)
            return JsonResponse(
                {"data": [professional_to_dict(p) for p in professionals]}, status=200
            )
        professional = get_object_or_404(HealthProfessional, pk=id, is_active=True)
        return JsonResponse({"data": professional_to_dict(professional)}, status=200)

    if request.method in {"POST", "PUT", "PATCH"}:
        data, error = _get_request_data(request)
        if error:
            return error
        if id is None and request.method != "POST":
            return _json_error("ID obrigatorio para atualizar.", status=400)
        instance = get_object_or_404(HealthProfessional, pk=id, is_active=True) if id else None
        form = MedForm(data, instance=instance)
        if form.is_valid():
            professional = form.save()
            status_code = 201 if instance is None else 200
            return JsonResponse({"data": professional_to_dict(professional)}, status=status_code)
        return _json_error("Erro de validacao.", status=400, details=form.errors)

    if request.method == "DELETE":
        if id is None:
            return _json_error("ID obrigatorio para excluir.", status=400)
        professional = get_object_or_404(HealthProfessional, pk=id, is_active=True)
        _soft_delete(professional)
        return JsonResponse({"data": {"deleted": True}}, status=200)

    return _json_error("Metodo nao permitido.", status=405)


@csrf_exempt
def exams_api(request, id=None):
    auth_error = _require_auth(request)
    if auth_error:
        return auth_error

    if request.method == "GET":
        if id is None:
            exams = MammogramExam.objects.filter(is_active=True)
            return JsonResponse({"data": [exam_to_dict(request, e) for e in exams]}, status=200)
        exam = get_object_or_404(MammogramExam, pk=id, is_active=True)
        return JsonResponse({"data": exam_to_dict(request, exam)}, status=200)

    if request.method in {"POST", "PUT", "PATCH"}:
        data, error = _get_request_data(request)
        if error:
            return error
        if id is None and request.method != "POST":
            return _json_error("ID obrigatorio para atualizar.", status=400)
        instance = get_object_or_404(MammogramExam, pk=id, is_active=True) if id else None
        form = MammogramExamForm(data, request.FILES, instance=instance)
        if form.is_valid():
            exam = form.save(commit=False)
            if instance is None:
                exam.user_ip = _get_client_ip(request)
            exam.save()
            form.save_m2m()
            status_code = 201 if instance is None else 200
            return JsonResponse({"data": exam_to_dict(request, exam)}, status=status_code)
        return _json_error("Erro de validacao.", status=400, details=form.errors)

    if request.method == "DELETE":
        if id is None:
            return _json_error("ID obrigatorio para excluir.", status=400)
        exam = get_object_or_404(MammogramExam, pk=id, is_active=True)
        _soft_delete(exam)
        return JsonResponse({"data": {"deleted": True}}, status=200)

    return _json_error("Metodo nao permitido.", status=405)
