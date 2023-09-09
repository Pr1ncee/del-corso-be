from django.apps import apps
from django.db import models
from django.utils import timezone

from base_models import BaseModel
from store.models.category import SeasonCategory, TypeCategory, Size, Color

from del_corso.config import general_config


class Product(BaseModel):
    name = models.CharField(max_length=100, verbose_name="Название")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    vendor_code = models.CharField(max_length=100, verbose_name="Артикул")
    new_collection = models.BooleanField(default=False)

    size = models.ForeignKey(Size, on_delete=models.CASCADE, verbose_name="Размер")
    color = models.ForeignKey(Color, on_delete=models.CASCADE, verbose_name="Цвет")
    season_category = models.ForeignKey(SeasonCategory, on_delete=models.CASCADE, verbose_name="Сезон")
    type_category = models.ForeignKey(TypeCategory, on_delete=models.CASCADE, verbose_name="Категория")

    def __str__(self):
        return f"{self.name} ({self.vendor_code}) - {self.price}"

    def get_current_price(self) -> float | models.DecimalField | int:
        """Get product's current price considering a discount"""

        product_discount_model = apps.get_model('discounts', 'ProductDiscount')
        active_discount = product_discount_model.objects.filter(
            product=self,
            discount__start_date__lte=timezone.now().date(),
            discount__end_date__gte=timezone.now().date()
        ).first()

        if active_discount:
            return active_discount.discount.discount_price
        return self.price

    class Meta:
        app_label = "store"
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    image = models.FileField(upload_to=general_config.TARGET_IMAGE_DIR, verbose_name="Изображение")
    primary = models.BooleanField(default=False, verbose_name="Основная фотография")

    def __str__(self):
        return f"{self.product.name} ({self.product.vendor_code}) - {self.product.price}"

    class Meta:
        app_label = "store"
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товаров"
