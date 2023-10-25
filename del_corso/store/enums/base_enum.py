from django.db.models import TextChoices


class BaseEnum(TextChoices):
    @classmethod
    def get_description(cls, enum_value):
        return dict(cls.choices).get(enum_value, enum_value)
