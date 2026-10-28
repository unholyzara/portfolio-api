import pytest
from django.conf import settings
from django.core.cache import cache
from django.urls import reverse


def throttle_limit():
    rate = settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]["login"]
    return int(rate.split("/")[0])


@pytest.mark.django_db
class TestCsrfTokenView:
    @pytest.fixture
    def url(self):
        return reverse("auth-csrf")

    def test_returns_token_to_anonymous_user(self, api_client, url):
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data["csrfToken"]

    def test_sets_csrf_cookie(self, api_client, url):
        response = api_client.get(url)
        assert settings.CSRF_COOKIE_NAME in response.cookies

    def test_post_not_allowed(self, api_client, url):
        assert api_client.post(url).status_code == 405


@pytest.mark.django_db
class TestLoginView:
    @pytest.fixture(autouse=True)
    def reset_throttle(self):
        cache.clear()

    @pytest.fixture
    def url(self):
        return reverse("auth-login")

    @pytest.fixture
    def post(self, api_client, url, email, password):
        def send(email=email, password=password):
            return api_client.post(
                url, {"email": email, "password": password}, format="json"
            )

        return send

    def test_staff_user_logs_in(self, api_client, staff_user, post, email):
        response = post()
        assert response.status_code == 200
        assert response.data["email"] == email
        assert api_client.session["_auth_user_id"] == str(staff_user.pk)

    @pytest.mark.parametrize(
        "raw", ["  STAFF@EXAMPLE.COM ", "Staff@Example.com"]
    )
    def test_email_is_stripped_and_case_insensitive(
        self, staff_user, post, email, raw
    ):
        response = post(email=raw)
        assert response.status_code == 200
        assert response.data["email"] == email

    def test_login_sets_csrf_cookie(self, staff_user, post):
        response = post()
        assert settings.CSRF_COOKIE_NAME in response.cookies

    @pytest.mark.parametrize(
        "e,p",
        [
            ("staff@example.com", "wrong"),
            ("nobody@example.com", "S3cure-passw0rd!"),
        ],
    )
    def test_invalid_credentials_are_rejected(
        self, api_client, staff_user, post, e, p
    ):
        response = post(email=e, password=p)
        assert response.status_code == 401
        assert "_auth_user_id" not in api_client.session

    @pytest.mark.parametrize(
        "extra",
        [{"is_staff": False}, {"is_staff": True, "is_active": False}],
    )
    def test_ineligible_user_is_rejected(
        self, api_client, make_user, post, extra
    ):
        make_user(email="other@example.com", **extra)
        response = post(email="other@example.com")
        assert response.status_code == 401
        assert "_auth_user_id" not in api_client.session

    def test_missing_credentials_are_rejected(self, api_client, url):
        assert api_client.post(url, {}, format="json").status_code == 401

    def test_get_not_allowed(self, api_client, url):
        assert api_client.get(url).status_code == 405

    def test_throttled_after_limit(self, staff_user, post):
        for _ in range(throttle_limit()):
            post(password="wrong")
        assert post(password="wrong").status_code == 429


@pytest.mark.django_db
class TestLogoutView:
    @pytest.fixture
    def url(self):
        return reverse("auth-logout")

    def test_logout_clears_session(self, api_client, staff_user, url):
        api_client.force_login(staff_user)
        response = api_client.post(url)
        assert response.status_code == 204
        assert "_auth_user_id" not in api_client.session

    def test_anonymous_user_is_forbidden(self, api_client, url):
        assert api_client.post(url).status_code == 403

    def test_missing_csrf_token_is_forbidden(
        self, csrf_client, staff_user, url
    ):
        csrf_client.force_login(staff_user)
        response = csrf_client.post(url)
        assert response.status_code == 403
        assert "_auth_user_id" in csrf_client.session

    def test_valid_csrf_token_allows_logout(self, csrf_client, staff_user, url):
        csrf_client.force_login(staff_user)
        token = csrf_client.get(reverse("auth-csrf")).data["csrfToken"]
        response = csrf_client.post(url, HTTP_X_CSRFTOKEN=token)
        assert response.status_code == 204
        assert "_auth_user_id" not in csrf_client.session

    def test_get_not_allowed(self, api_client, staff_user, url):
        api_client.force_login(staff_user)
        assert api_client.get(url).status_code == 405
