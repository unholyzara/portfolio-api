from typing import TypeVar

from django.db.models import Model

ModelType = TypeVar("ModelType", bound=Model)
