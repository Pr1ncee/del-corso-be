from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from base_models import BaseModel


class SeasonCategory(BaseModel):
    name = models.CharField(max_length=20, verbose_name="Название")

    class Meta:
        app_label = "store"
        verbose_name = "Сезон"
        verbose_name_plural = "Сезоны"

    def __str__(self):
        return self.name


class TypeCategory(BaseModel):
    name = models.CharField(max_length=20, verbose_name="Название")
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
            MinValueValidator(36, message="Допустимый размер: 36-40."),
            MaxValueValidator(40, message="Допустимый размер: 36-40."),
        ],
        verbose_name="Размер"
    )

    def __str__(self):
        return str(self.size)

    class Meta:
        app_label = "store"
        verbose_name = "Размер"
        verbose_name_plural = "Размеры"


class Color(BaseModel):
    color = models.CharField(max_length=20, verbose_name="Цвет")

    def __str__(self):
        return self.color

    class Meta:
        app_label = "store"
        verbose_name = "Цвет"
        verbose_name_plural = "Цвета"
