from django.test import RequestFactory, SimpleTestCase, override_settings

from apps.api.handlers.common import get_client_ip
from apps.exams.forms import MammogramExamForm


class GetClientIpTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @override_settings(TRUSTED_PROXY_IPS=["10.0.0.10"])
    def test_uses_forwarded_for_when_remote_addr_is_trusted_proxy(self):
        request = self.factory.get(
            "/",
            HTTP_X_FORWARDED_FOR="198.51.100.25, 10.0.0.10",
            REMOTE_ADDR="10.0.0.10",
        )

        self.assertEqual(get_client_ip(request), "198.51.100.25")

    @override_settings(TRUSTED_PROXY_IPS=["10.0.0.10"])
    def test_ignores_forwarded_for_when_remote_addr_is_not_trusted_proxy(self):
        request = self.factory.get(
            "/",
            HTTP_X_FORWARDED_FOR="198.51.100.25",
            REMOTE_ADDR="203.0.113.9",
        )

        self.assertEqual(get_client_ip(request), "203.0.113.9")

    @override_settings(TRUSTED_PROXY_IPS=["10.0.0.10"])
    def test_falls_back_to_remote_addr_when_forwarded_for_is_invalid(self):
        request = self.factory.get(
            "/",
            HTTP_X_FORWARDED_FOR="not-an-ip",
            REMOTE_ADDR="10.0.0.10",
        )

        self.assertEqual(get_client_ip(request), "10.0.0.10")


class MammogramExamFormTests(SimpleTestCase):
    def test_user_ip_is_not_exposed_in_form(self):
        self.assertNotIn("user_ip", MammogramExamForm.base_fields)
