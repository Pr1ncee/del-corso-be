import logging

from django.db import models
from django.shortcuts import get_object_or_404

from base_models import BaseModel
from del_corso import setup_logging
from store.models.product import Product

setup_logging()
logger = logging.getLogger(__name__)


class Discount(BaseModel):
    name = models.CharField(
        max_length=100,
        verbose_name="Название",
        help_text="Название представляет собой артикул товара, на который Вы хотите создать скидку"
    )
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена со скидкой")
    start_date = models.DateField(verbose_name="Дата начала акции")
    end_date = models.DateField(verbose_name="Дата конца акции")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_new = self.pk
        super().save(*args, **kwargs)

        logger.info(
            f"Discount object {self.name} updated. Discount price - {self.discount_price}"
        )
        if not is_new:
            logger.info("Creating ProductDiscount object...")
            product = get_object_or_404(Product, vendor_code=self.name)
            product_discount = ProductDiscount.objects.create(product=product, discount=self)
            logger.info(f"ProductDiscount object {product_discount.id} created successfully!")

    class Meta:
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"


class ProductDiscount(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, verbose_name="Скидка")

    def __str__(self):
        return f"{self.discount.name} on {self.product.name}"

    class Meta:
        verbose_name = "Скидка на товар"
        verbose_name_plural = "Скидки на товары"
