from colorfield.fields import ColorField
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models

from base_models import BaseModel


class SeasonCategory(BaseModel):
    name = models.CharField(max_length=20, verbose_name="Название", unique=True, null=False)

    class Meta:
        app_label = "store"
        verbose_name = "Сезон"
        verbose_name_plural = "Сезоны"

    def __str__(self):
        return self.name


class TypeCategory(BaseModel):
    name = models.CharField(max_length=20, verbose_name="Название", unique=True, null=False)
    is_popular = models.BooleanField(default=False, verbose_name="Популярная категория")

    class Meta:
        app_label = "store"
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Size(BaseModel):
    size = models.IntegerField(
        validators=[
            MinValueValidator(35, message="Допустимый размер: 35-41."),
            MaxValueValidator(41, message="Допустимый размер: 35-41."),
        ],
        verbose_name="Размер",
        unique=True,
        null=False
    )

    def __str__(self):
        return str(self.size)

    class Meta:
        app_label = "store"
        verbose_name = "Размер"
        verbose_name_plural = "Размеры"


class Color(BaseModel):
    color = models.CharField(max_length=20, verbose_name="Цвет", unique=True, null=False)
    hex_number = ColorField(
        verbose_name="Выберите цвет",
        validators=[
            RegexValidator(regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
        ]
    )

    def __str__(self):
        return self.color

    class Meta:
        app_label = "store"
        verbose_name = "Цвет"
        verbose_name_plural = "Цвета"
