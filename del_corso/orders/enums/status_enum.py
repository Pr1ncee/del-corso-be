from django.db import models


class OrderStatus(models.TextChoices):
    PENDING = 'Pending', 'В ожидании обработки'
    PROCESSING = 'Processing', 'Обрабатывается'
    SHIPPED = 'Shipped', 'Передан курьеру'
    DELIVERED = 'Delivered', 'Доставлен'
    CANCELED = 'Canceled', 'Отменен'
