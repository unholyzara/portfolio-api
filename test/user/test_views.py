from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

EMAIL = "staff@example.com"
PASSWORD = "S3cure-passw0rd!"


def create_user(email=EMAIL, password=PASSWORD, **extra):
    return get_user_model().objects.create_user(
        email=email, password=password, **extra
    )


def throttle_limit():
    rate = settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]["login"]
    return int(rate.split("/")[0])


class CsrfTokenViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("auth-csrf")

    def test_returns_token_to_anonymous_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["csrfToken"])

    def test_sets_csrf_cookie(self):
        response = self.client.get(self.url)
        self.assertIn(settings.CSRF_COOKIE_NAME, response.cookies)

    def test_post_not_allowed(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)


class LoginViewTestCase(APITestCase):
    def setUp(self):
        cache.clear()
        self.url = reverse("auth-login")
        self.user = create_user(is_staff=True)

    def post(self, email=EMAIL, password=PASSWORD):
        return self.client.post(
            self.url, {"email": email, "password": password}, format="json"
        )

    def test_staff_user_logs_in(self):
        response = self.post()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["email"], EMAIL)
        self.assertEqual(
            self.client.session["_auth_user_id"], str(self.user.pk)
        )

    def test_email_is_stripped_and_lowercased(self):
        response = self.post(email="  STAFF@EXAMPLE.COM ")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["email"], EMAIL)

    def test_login_sets_csrf_cookie(self):
        response = self.post()
        self.assertIn(settings.CSRF_COOKIE_NAME, response.cookies)

    def test_wrong_password_is_rejected(self):
        response = self.post(password="wrong")
        self.assertEqual(response.status_code, 401)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_unknown_email_is_rejected(self):
        response = self.post(email="nobody@example.com")
        self.assertEqual(response.status_code, 401)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_non_staff_user_is_rejected(self):
        create_user(email="visitor@example.com", is_staff=False)
        response = self.post(email="visitor@example.com")
        self.assertEqual(response.status_code, 401)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_inactive_user_is_rejected(self):
        create_user(
            email="inactive@example.com", is_staff=True, is_active=False
        )
        response = self.post(email="inactive@example.com")
        self.assertEqual(response.status_code, 401)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_missing_credentials_are_rejected(self):
        response = self.client.post(self.url, {}, format="json")
        self.assertEqual(response.status_code, 401)

    def test_get_not_allowed(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_throttled_after_limit(self):
        for _ in range(throttle_limit()):
            self.post(password="wrong")
        response = self.post(password="wrong")
        self.assertEqual(response.status_code, 429)


class LogoutViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("auth-logout")
        self.user = create_user(is_staff=True)

    def test_logout_clears_session(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 204)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_anonymous_user_is_forbidden(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)

    def test_missing_csrf_token_is_forbidden(self):
        client = APIClient(enforce_csrf_checks=True)
        client.force_login(self.user)
        response = client.post(self.url)
        self.assertEqual(response.status_code, 403)
        self.assertIn("_auth_user_id", client.session)

    def test_valid_csrf_token_allows_logout(self):
        client = APIClient(enforce_csrf_checks=True)
        client.force_login(self.user)
        token = client.get(reverse("auth-csrf")).data["csrfToken"]
        response = client.post(self.url, HTTP_X_CSRFTOKEN=token)
        self.assertEqual(response.status_code, 204)
        self.assertNotIn("_auth_user_id", client.session)

    def test_get_not_allowed(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
