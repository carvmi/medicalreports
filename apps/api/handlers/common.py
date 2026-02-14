import json
from ipaddress import ip_address

from django.http import JsonResponse, QueryDict
from django.conf import settings
from django.utils import timezone


def json_error(message, status=400, details=None):
    payload = {"error": message}
    if details is not None:
        payload["details"] = details
    return JsonResponse(payload, status=status)


def require_auth(request):
    if not request.user.is_authenticated:
        return json_error("Autenticacao necessaria.", status=401)
    return None


def parse_json_body(request):
    raw = request.body.decode("utf-8") if request.body else ""
    if not raw:
        return {}, None
    try:
        return json.loads(raw), None
    except json.JSONDecodeError:
        return None, json_error("JSON invalido.", status=400)


def get_request_data(request):
    content_type = request.content_type or ""
    if "application/json" in content_type:
        data, error = parse_json_body(request)
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


def as_date(value):
    return value.isoformat() if value else None


def as_datetime(value):
    return value.isoformat() if value else None


def build_file_url(request, file_field):
    if not file_field:
        return None
    try:
        return request.build_absolute_uri(file_field.url)
    except Exception:
        return None


def get_client_ip(request):
    remote_addr = request.META.get("REMOTE_ADDR")
    if not remote_addr:
        return None

    try:
        ip_address(remote_addr)
    except ValueError:
        return None

    trusted_proxy_ips = set(getattr(settings, "TRUSTED_PROXY_IPS", []))
    if remote_addr in trusted_proxy_ips:
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "")
        forwarded_ip = x_forwarded_for.split(",")[0].strip() if x_forwarded_for else ""
        if forwarded_ip:
            try:
                ip_address(forwarded_ip)
                return forwarded_ip
            except ValueError:
                pass

    return remote_addr


def soft_delete(instance):
    instance.is_active = False
    instance.deleted_at = timezone.now()
    instance.save(update_fields=["is_active", "deleted_at"])
