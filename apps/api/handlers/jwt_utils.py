import base64
import hashlib
import hmac
import json
from datetime import datetime, timedelta, timezone

from django.conf import settings


class JWTError(Exception):
    pass


class ExpiredSignatureError(JWTError):
    pass


class InvalidTokenError(JWTError):
    pass


def _get_now():
    return datetime.now(timezone.utc)


def _b64url_encode(data):
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(value):
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode((value + padding).encode("ascii"))


def _sign(data):
    return hmac.new(
        settings.JWT_SECRET_KEY.encode("utf-8"),
        data.encode("ascii"),
        hashlib.sha256,
    ).digest()


def _encode_token(payload):
    if settings.JWT_ALGORITHM != "HS256":
        raise InvalidTokenError("Algoritmo JWT nao suportado.")

    header = {"alg": "HS256", "typ": "JWT"}
    header_segment = _b64url_encode(
        json.dumps(header, separators=(",", ":"), sort_keys=True).encode("utf-8")
    )
    payload_segment = _b64url_encode(
        json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    )
    signing_input = f"{header_segment}.{payload_segment}"
    signature_segment = _b64url_encode(_sign(signing_input))
    return f"{signing_input}.{signature_segment}"


def _decode_token(token):
    try:
        header_segment, payload_segment, signature_segment = token.split(".")
    except ValueError as exc:
        raise InvalidTokenError("Formato de token invalido.") from exc

    signing_input = f"{header_segment}.{payload_segment}"
    expected_signature = _sign(signing_input)
    try:
        provided_signature = _b64url_decode(signature_segment)
    except Exception as exc:
        raise InvalidTokenError("Assinatura invalida.") from exc

    if not hmac.compare_digest(expected_signature, provided_signature):
        raise InvalidTokenError("Assinatura invalida.")

    try:
        header = json.loads(_b64url_decode(header_segment).decode("utf-8"))
        payload = json.loads(_b64url_decode(payload_segment).decode("utf-8"))
    except Exception as exc:
        raise InvalidTokenError("Token malformado.") from exc

    if header.get("alg") != "HS256":
        raise InvalidTokenError("Algoritmo JWT invalido.")

    return payload


def _base_payload(user, token_type, expires_delta):
    now = _get_now()
    return {
        "sub": str(user.id),
        "username": user.username,
        "token_type": token_type,
        "iat": int(now.timestamp()),
        "exp": int((now + expires_delta).timestamp()),
        "iss": settings.JWT_ISSUER,
    }


def create_access_token(user):
    payload = _base_payload(
        user,
        token_type="access",
        expires_delta=timedelta(minutes=settings.JWT_ACCESS_TOKEN_LIFETIME_MINUTES),
    )
    return _encode_token(payload)


def create_refresh_token(user):
    payload = _base_payload(
        user,
        token_type="refresh",
        expires_delta=timedelta(days=settings.JWT_REFRESH_TOKEN_LIFETIME_DAYS),
    )
    return _encode_token(payload)


def decode_token(token, expected_token_type):
    payload = _decode_token(token)
    if payload.get("iss") != settings.JWT_ISSUER:
        raise InvalidTokenError("Issuer invalido.")

    exp = payload.get("exp")
    if not isinstance(exp, int):
        raise InvalidTokenError("Claim exp invalida.")
    if exp < int(_get_now().timestamp()):
        raise ExpiredSignatureError("Token expirado.")

    if payload.get("token_type") != expected_token_type:
        raise InvalidTokenError("Tipo de token invalido.")
    return payload
