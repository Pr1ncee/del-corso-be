from django.db import models


class UpperMaterialType(models.TextChoices):
    GENUINE_LEATHER = "Genuine leather", "Натуральная кожа"


class LiningMaterialType(models.TextChoices):
    NATURAL_FUR = "Natural fur", "Натуральный мех"
    BAIZE = "Baize", "Байка"


class CompletenessType(models.TextChoices):
    AVERAGE = "Average", "Средняя"


class TrueToSizeType(models.TextChoices):
    EXACT_SIZE = "Exact size", "Размер в размер"
