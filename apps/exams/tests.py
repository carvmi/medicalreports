from datetime import date

from django.test import RequestFactory, SimpleTestCase, TestCase, override_settings

from apps.api.handlers.common import get_client_ip
from apps.exams.forms import MammogramExamForm
from apps.institution.models import Institution
from apps.patients.models import Patient


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


class MammogramExamFormQuerysetTests(TestCase):
    def test_patient_and_local_fields_only_include_active_records(self):
        active_patient = Patient.objects.create(full_name="Ativa", birth_date=date(1990, 1, 1), is_active=True)
        Patient.objects.create(full_name="Inativa", birth_date=date(1991, 1, 1), is_active=False)

        active_local = Institution.objects.create(
            name="Clinica Ativa",
            phone="81999999999",
            email="ativa@example.com",
            is_active=True,
        )
        Institution.objects.create(
            name="Clinica Inativa",
            phone="81888888888",
            email="inativa@example.com",
            is_active=False,
        )

        form = MammogramExamForm()

        self.assertQuerySetEqual(
            form.fields["patient"].queryset.order_by("id"),
            [active_patient],
            transform=lambda x: x,
        )
        self.assertQuerySetEqual(
            form.fields["local"].queryset.order_by("id"),
            [active_local],
            transform=lambda x: x,
        )
