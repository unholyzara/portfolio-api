from enum import Enum
from dataclasses import dataclass

from django.db.models import Model
from rest_framework import mixins, generics, permissions, serializers, viewsets
from rest_framework.routers import BaseRouter

from api.utils.models import ActiveModel


class Actions(Enum):
    LIST = mixins.ListModelMixin
    RETRIEVE = mixins.RetrieveModelMixin
    CREATE = mixins.CreateModelMixin
    UPDATE = mixins.UpdateModelMixin
    DESTROY = mixins.DestroyModelMixin


WRITE_ACTIONS = (Actions.CREATE, Actions.UPDATE, Actions.DESTROY)
PUBLIC_ACTIONS = (Actions.LIST, Actions.RETRIEVE)


class ActiveFilterMixin(generics.GenericAPIView):
    def get_queryset(self):
        queryset = super().get_queryset()
        if issubclass(queryset.model, ActiveModel):
            queryset = queryset.filter(active=True)
        return queryset


@dataclass
class ModelViews:
    model: type[Model]
    read_serializer: type[serializers.ModelSerializer]
    write_serializer: type[serializers.ModelSerializer] | None = None
    actions: tuple[Actions, ...] = PUBLIC_ACTIONS
    select_related: tuple[str, ...] = ()
    prefetch_related: tuple[str, ...] = ()
    lookup_field: str = "uuid"

    def _viewset(self) -> type[viewsets.GenericViewSet]:
        config = self
        queryset = self.model.objects.select_related(
            *self.select_related
        ).prefetch_related(*self.prefetch_related)

        class View(
            ActiveFilterMixin,
            *(action.value for action in self.actions),
            viewsets.GenericViewSet,
        ):
            lookup_field = config.lookup_field

            def get_serializer_class(self):
                if self.action in WRITE_ACTIONS and config.write_serializer:
                    return config.write_serializer
                return config.read_serializer

            def get_permissions(self):
                if self.action in PUBLIC_ACTIONS:
                    return [permissions.AllowAny()]
                return [permissions.IsAdminUser()]

        View.queryset = queryset
        View.__name__ = f"{self.model.__name__}ViewSet"
        return View

    def register(self, router: BaseRouter, prefix: str) -> None:
        router.register(
            prefix, self._viewset(), basename=self.model._meta.model_name
        )
