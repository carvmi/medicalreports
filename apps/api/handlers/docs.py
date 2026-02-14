from pathlib import Path

from django.conf import settings
from django.http import HttpResponse

from .common import json_error


def docs_api(request):
    if request.method != "GET":
        return json_error("Metodo nao permitido.", status=405)

    docs_path = Path(settings.BASE_DIR) / "MRAPI-documentation.html"
    if not docs_path.exists():
        return json_error("Arquivo de documentacao nao encontrado.", status=404)

    return HttpResponse(
        docs_path.read_text(encoding="utf-8"),
        content_type="text/html; charset=utf-8",
    )

