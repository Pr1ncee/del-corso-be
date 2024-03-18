import logging

from django.core.validators import EmailValidator
from django.db import models
from django.db.models import Sum

from base_models import BaseModel
from del_corso import setup_logging
from orders.enums.status_enum import OrderStatus
from store.models.product import Product
from store.validators import validate_phone_number

setup_logging()
logger = logging.getLogger(__name__)


class Order(BaseModel):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    surname = models.CharField(max_length=100, verbose_name="Отчество")
    country = models.CharField(max_length=50, verbose_name="Страна")
    telephone_number = models.CharField(max_length=20, validators=[validate_phone_number], verbose_name="Номер телефона")
    email = models.EmailField(
        validators=[
            EmailValidator(message='Введите действительный адрес электронной почты.'),
        ],
        verbose_name="Электронный адрес",
        blank=True,
        null=True
    )
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий к заказу")
    address = models.TextField(verbose_name="Адрес")

    order_date = models.DateField(verbose_name="Дата заказа")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Цена заказа")

    status = models.CharField(max_length=50, choices=OrderStatus.choices, default=OrderStatus.PENDING, verbose_name="Статус")

    def update_total_amount(self):
        total_amount = OrderItem.objects.filter(order=self).aggregate(Sum('subtotal'))['subtotal__sum']
        self.total_amount = total_amount
        self.save()
        logger.info(f"Order {self.id} updated with total amount: {total_amount}")

    def __str__(self):
        return f"{self.last_name} {self.first_name} - {self.telephone_number}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Итоговая сумма")
    size = models.IntegerField(verbose_name="Размер", null=True)

    def __str__(self):
        return (f"{self.order.last_name} {self.order.first_name} {self.order.surname} "
                f"- {self.order.telephone_number}. {self.product.name} ({self.product.vendor_code}) - {self.quantity}")

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.product.get_current_price()
        super().save(*args, **kwargs)
        logger.info(f"OrderItem {self.pk} updated. Related Order - {self.order.id}")

        self.order.update_total_amount()

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказов"
