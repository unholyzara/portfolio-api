from collections.abc import Mapping

from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_protect
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
    throttle_classes,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from .throttles import LoginThrottle, LoginEmailThrottle


@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def csrf_token(request: Request) -> Response:
    return Response({"csrfToken": get_token(request)})


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
@throttle_classes([LoginThrottle, LoginEmailThrottle])
@csrf_protect
def login_view(request: Request) -> Response:
    payload = request.data
    if not isinstance(payload, Mapping):
        return Response(status=400)
    user = authenticate(
        request,
        email=str(payload.get("email", "")),
        password=payload.get("password"),
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
