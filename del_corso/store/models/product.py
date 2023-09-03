from django.db import models

from base_models import BaseModel
from store.models.category import SeasonCategory, TypeCategory, Size, Color

from del_corso.config import general_config


class Product(BaseModel):
    name = models.CharField(max_length=100, verbose_name="Название")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    vendor_code = models.CharField(max_length=100, verbose_name="Артикул")

    size = models.ForeignKey(Size, on_delete=models.CASCADE, verbose_name="Размер")
    color = models.ForeignKey(Color, on_delete=models.CASCADE, verbose_name="Цвет")
    season_category = models.ForeignKey(SeasonCategory, on_delete=models.CASCADE, verbose_name="Сезон")
    type_category = models.ForeignKey(TypeCategory, on_delete=models.CASCADE, verbose_name="Категория")

    def __str__(self):
        return f"{self.name} ({self.vendor_code}) - {self.price}"

    class Meta:
        app_label = "store"
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    image = models.FileField(upload_to=general_config.TARGET_IMAGE_DIR, verbose_name="Изображение")

    def __str__(self):
        return f"{self.product.name} ({self.product.vendor_code}) - {self.product.price}"

    class Meta:
        app_label = "store"
        verbose_name = "Изображение продукта"
        verbose_name_plural = "Изображения продуктов"
