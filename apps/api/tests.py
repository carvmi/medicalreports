from django.contrib.auth.models import User
from django.test import TestCase


class APIJWTAuthTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="apiuser",
            email="apiuser@example.com",
            password="StrongPass123!",
        )

    def test_login_returns_access_and_refresh_tokens(self):
        response = self.client.post(
            "/api/auth/login",
            data={"username": "apiuser", "password": "StrongPass123!"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()["data"]
        self.assertIn("access", payload)
        self.assertIn("refresh", payload)
        self.assertEqual(payload["token_type"], "Bearer")

    def test_me_requires_authentication(self):
        response = self.client.get("/api/auth/me")
        self.assertEqual(response.status_code, 401)

    def test_me_accepts_bearer_access_token(self):
        login_response = self.client.post(
            "/api/auth/login",
            data={"username": "apiuser", "password": "StrongPass123!"},
            content_type="application/json",
        )
        access = login_response.json()["data"]["access"]

        response = self.client.get(
            "/api/auth/me",
            HTTP_AUTHORIZATION=f"Bearer {access}",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["username"], self.user.username)

    def test_refresh_returns_new_access_token(self):
        login_response = self.client.post(
            "/api/auth/login",
            data={"username": "apiuser", "password": "StrongPass123!"},
            content_type="application/json",
        )
        refresh = login_response.json()["data"]["refresh"]

        refresh_response = self.client.post(
            "/api/auth/refresh",
            data={"refresh": refresh},
            content_type="application/json",
        )

        self.assertEqual(refresh_response.status_code, 200)
        self.assertIn("access", refresh_response.json()["data"])

