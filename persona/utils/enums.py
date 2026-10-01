from enum import Enum


class DjangoEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class Levels(DjangoEnum):
    LW = "Basso"
    ML = "Medio-Basso"
    MD = "Medio"
    MA = "Medio-Avanzato"
    AD = "Avanzato"
