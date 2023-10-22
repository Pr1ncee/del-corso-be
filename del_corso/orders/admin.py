from django.contrib import admin
from django.utils.html import format_html

from orders.enums.status_enum import OrderStatus
from orders.models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ("id", "first_name", "last_name", "surname", "country",
                    "telephone_number", "email", "truncated_address", "order_date", "colored_status")
    search_fields = ("id", "first_name", "last_name", "surname", "country",
                     "telephone_number", "email", "address", "order_date", "status")

    def colored_status(self, obj):
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

    def truncated_address(self, obj):
        max_length = 25
        if len(obj.address) > max_length:
            return obj.address[:max_length] + "..."
        return obj.address

    truncated_address.short_description = "Address"


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


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)

