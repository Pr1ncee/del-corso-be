import logging

from django.contrib import admin
from django.utils.html import format_html

from del_corso import setup_logging
from orders.enums.status_enum import OrderStatus
from orders.forms import OrderStatusForm
from orders.models import Order, OrderItem

setup_logging()
logger = logging.getLogger(__name__)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ("id", "first_name", "last_name", "surname", "country",
                    "telephone_number", "email", "truncated_address", "order_date", "colored_status")
    search_fields = ("id", "first_name", "last_name", "surname", "country",
                     "telephone_number", "email", "address", "order_date", "status")
    list_filter = ("status", )
    action_form = OrderStatusForm
    actions = ("change_status", )

    def colored_status(self, obj: Order):
        status_russian = obj.get_status_display()

        status_colors = {
            OrderStatus.PENDING: 'orange',
            OrderStatus.PROCESSING: 'blue',
            OrderStatus.SHIPPED: 'purple',
            OrderStatus.DELIVERED: 'green',
            OrderStatus.CANCELED: 'red',
        }

        status = obj.status
        color = status_colors.get(status, 'white')

        return format_html(f'<span style="color: {color};">{status_russian}</span>')
    colored_status.short_description = "Статус"

    def truncated_address(self, obj: Order) -> str:
        max_length = 25
        if len(obj.address) > max_length:
            return obj.address[:max_length] + "..."
        return obj.address
    truncated_address.short_description = "Адрес"

    @admin.action(description="Изменить статус заказа")
    def change_status(self, request, queryset: list[Order]) -> None:
        desired_status = OrderStatus[request.POST["status"].upper()]
        queryset.update(status=desired_status)
        logging.info(f"Updated {len(queryset)} Order objects with new status: {desired_status}")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    model = OrderItem
    list_display = ("id", "order", "product", "quantity", "subtotal", "is_product_in_stock")
    search_fields = ("id", "subtotal", "quantity")

    @admin.display(
        boolean=True
    )
    def is_product_in_stock(self, obj):
        return obj.product.in_stock

    is_product_in_stock.short_description = "В наличии"
