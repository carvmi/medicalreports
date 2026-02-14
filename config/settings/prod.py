import os

from .base import *

DEBUG = False

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", SECRET_KEY)

allowed_hosts = os.getenv("DJANGO_ALLOWED_HOSTS", "")
ALLOWED_HOSTS = [host.strip() for host in allowed_hosts.split(",") if host.strip()]

trust_proxy_headers = os.getenv("DJANGO_TRUST_PROXY_HEADERS", "0") == "1"
if trust_proxy_headers:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    USE_X_FORWARDED_HOST = True
