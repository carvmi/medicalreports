from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .common import get_request_data, json_error, require_auth


@csrf_exempt
def register_api(request):
    if request.method != "POST":
        return json_error("Metodo nao permitido.", status=405)
    data, error = get_request_data(request)
    if error:
        return error
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not password:
        return json_error("username e password sao obrigatorios.", status=400)

    if User.objects.filter(username=username).exists():
        return json_error("Usuario ja existe.", status=400)

    user = User.objects.create_user(username=username, email=email, password=password)
    return JsonResponse(
        {"data": {"id": user.id, "username": user.username, "email": user.email}},
        status=201,
    )


@csrf_exempt
def login_api(request):
    if request.method != "POST":
        return json_error("Metodo nao permitido.", status=405)
    data, error = get_request_data(request)
    if error:
        return error
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return json_error("username e password sao obrigatorios.", status=400)

    user = authenticate(request, username=username, password=password)
    if user is None:
        return json_error("Usuario ou senha invalidos.", status=401)

    auth_login(request, user)
    token = request.session.session_key
    if not token:
        request.session.save()
        token = request.session.session_key
    return JsonResponse(
        {
            "data": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "token": token,
            }
        },
        status=200,
    )


def me_api(request):
    auth_error = require_auth(request)
    if auth_error:
        return auth_error
    user = request.user
    return JsonResponse(
        {"data": {"id": user.id, "username": user.username, "email": user.email}},
        status=200,
    )

