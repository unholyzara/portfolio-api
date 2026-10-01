from dataclasses import dataclass
from uuid import UUID

from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from api.utils.models import ActiveModel


def get_active_object[MT: ActiveModel](
    model: type[MT], uuid_value: str | None, fe_flag: bool
) -> MT:
    try:
        object_uuid = UUID(uuid_value)
    except (AttributeError, TypeError, ValueError):
        raise Http404
    obj = get_object_or_404(model, uuid=object_uuid)
    if fe_flag and not obj.active:
        raise Http404
    return obj


@dataclass
class ActiveModelViews[MT: ActiveModel, ST: serializers.ModelSerializer]:
    model: type[MT]
    serializer: type[ST]

    def list_endpoint(self, fe_flag: bool = False):
        @api_view(["GET"])
        def endpoint(request: Request) -> Response:
            model_objects = self.model.objects.all()
            if fe_flag:
                model_objects = model_objects.filter(active=True)
            serialized = self.serializer(model_objects, many=True)
            return Response(serialized.data)

        return endpoint

    def detail_endpoint(self, fe_flag: bool = False):
        @api_view(["GET"])
        def endpoint(request: Request) -> Response:
            model_obj = get_active_object(
                self.model, request.query_params.get("uuid"), fe_flag=fe_flag
            )
            serialized = self.serializer(model_obj)
            return Response(serialized.data)

        return endpoint
