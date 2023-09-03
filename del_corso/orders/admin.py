from django.contrib import admin

from orders.models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    model = Order


class OrderItemAdmin(admin.ModelAdmin):
    model = OrderItem


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)

