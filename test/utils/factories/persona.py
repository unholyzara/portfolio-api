import uuid
import factory
from persona.models import Overview


class OverviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Overview

    uuid = factory.Sequence(lambda n: uuid.UUID(int=n + 1))
    text = factory.Sequence(lambda n: f"overview-text-{n}")
    active = True
