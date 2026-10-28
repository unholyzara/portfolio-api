import hashlib

from collections.abc import Mapping

from rest_framework.throttling import AnonRateThrottle, SimpleRateThrottle


class LoginThrottle(AnonRateThrottle):
    scope = "login"


class LoginEmailThrottle(SimpleRateThrottle):
    scope = "login_email"

    def get_cache_key(self, request, view):
        payload = request.data
        if not isinstance(payload, Mapping):
            return None
        email = payload.get("email")

        if not isinstance(email, str) or not email.strip():
            return None

        normalized_email = email.strip().casefold()
        ident = hashlib.sha256(normalized_email.encode("utf-8")).hexdigest()

        return self.cache_format % {
            "scope": self.scope,
            "ident": ident,
        }
