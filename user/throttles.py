import hashlib

from rest_framework.throttling import AnonRateThrottle, SimpleRateThrottle


class LoginThrottle(AnonRateThrottle):
    scope = "login"


class LoginEmailThrottle(SimpleRateThrottle):
    scope = "login_email"

    def get_cache_key(self, request, view):
        email = request.data.get("email")

        if not isinstance(email, str) or not email.strip():
            return None

        normalized_email = email.strip().casefold()
        ident = hashlib.sha256(normalized_email.encode("utf-8")).hexdigest()

        return self.cache_format % {
            "scope": self.scope,
            "ident": ident,
        }
