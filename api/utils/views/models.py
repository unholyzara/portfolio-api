import abc

from enum import Enum
from dataclasses import dataclass

from django.db.models import Model, Prefetch
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
        user = self.request.user
        is_staff = bool(user.is_authenticated and user.is_staff)
        if not is_staff and issubclass(queryset.model, ActiveModel):
            queryset = queryset.filter(active=True)
        return queryset


@dataclass
class AbstractModelViews(abc.ABC):
    model: type[Model]
    read_serializer: type[serializers.ModelSerializer]
    select_related: tuple[str, ...] = ()
    prefetch_related: tuple[str, ...] = ()
    lookup_field: str = "uuid"

    @abc.abstractmethod
    def _viewset(self) -> type[viewsets.GenericViewSet]:
        pass

    def register(self, router: BaseRouter, prefix: str) -> None:
        router.register(prefix, self._viewset(), basename=prefix)


@dataclass
class ModelViews(AbstractModelViews):
    actions: tuple[Actions, ...] = PUBLIC_ACTIONS

    def _viewset(self) -> type[viewsets.GenericViewSet]:
        config = self
        queryset = self.model.objects.select_related(*self.select_related)

        class View(
            ActiveFilterMixin,
            *(action.value for action in self.actions),
            viewsets.GenericViewSet,
        ):
            lookup_field = config.lookup_field

            def get_queryset(self):
                queryset = super().get_queryset().prefetch_related(None)
                lookups = []
                for name in config.prefetch_related:
                    related = config.model._meta.get_field(name).related_model
                    lookups.append(
                        Prefetch(
                            name,
                            queryset=related.objects.filter(active=True),
                        )
                    )
                return queryset.prefetch_related(*lookups)

            def get_serializer_class(self):
                return config.read_serializer

            def get_permissions(self):
                return [permissions.AllowAny()]

        View.queryset = queryset
        View.__name__ = f"{self.model.__name__}ViewSet"
        return View


@dataclass(kw_only=True)
class StaffModelViews(AbstractModelViews):
    write_serializer: type[serializers.ModelSerializer]
    actions: tuple[Actions, ...] = PUBLIC_ACTIONS + WRITE_ACTIONS

    def _viewset(self) -> type[viewsets.GenericViewSet]:
        config = self
        queryset = self.model.objects.select_related(*self.select_related)

        class View(
            *(action.value for action in self.actions),
            viewsets.GenericViewSet,
        ):
            lookup_field = config.lookup_field

            def get_queryset(self):
                queryset = super().get_queryset().prefetch_related(None)
                return queryset.prefetch_related(*config.prefetch_related)

            def get_serializer_class(self):
                if (
                    self.action in [a.name.lower() for a in WRITE_ACTIONS]
                    and config.write_serializer
                ):
                    return config.write_serializer
                return config.read_serializer

            def get_permissions(self):
                return [permissions.IsAdminUser()]

        View.queryset = queryset
        View.__name__ = f"{self.model.__name__}StaffViewSet"
        return View
