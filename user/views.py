from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
    throttle_classes,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle


class LoginThrottle(AnonRateThrottle):
    scope = "login"


@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def csrf_token(request: Request) -> Response:
    return Response({"csrfToken": get_token(request)})


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
@throttle_classes([LoginThrottle])
def login_view(request: Request) -> Response:
    user = authenticate(
        request,
        email=str(request.data.get("email", "")),
        password=request.data.get("password"),
    )
    if user is None or not user.is_staff:
        return Response(status=401)
    login(request, user)
    return Response({"email": user.email})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request: Request) -> Response:
    logout(request)
    return Response(status=204)
