import os

from .base import *

DEBUG = True

allowed_hosts = os.getenv(
    "DJANGO_ALLOWED_HOSTS",
    "localhost,127.0.0.1,0.0.0.0,[::1],*",
)
ALLOWED_HOSTS = [host.strip() for host in allowed_hosts.split(",") if host.strip()]

# Local reverse proxies (nginx/caddy on same host) usually connect from loopback.
if not TRUSTED_PROXY_IPS:
    TRUSTED_PROXY_IPS = ["127.0.0.1", "::1"]
