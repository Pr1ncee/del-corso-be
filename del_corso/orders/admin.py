from django.contrib import admin

from orders.models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ("id", "first_name", "last_name", "surname", "country",
                    "telephone_number", "email", "address", "order_date")
    search_fields = ("id", "first_name", "last_name", "surname", "country",
                     "telephone_number", "email", "address", "order_date")


class OrderItemAdmin(admin.ModelAdmin):
    model = OrderItem
    list_display = ("id", "order", "product", "quantity", "subtotal")
    search_fields = ("id", "subtotal", "quantity")


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)

