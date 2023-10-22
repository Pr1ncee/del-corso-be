import logging

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from orders.models import Order, OrderItem
from store.models import Product

logger = logging.getLogger(__name__)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ("product", "quantity", "subtotal")


class OrderSerializer(serializers.ModelSerializer):
    product_quantities = serializers.ListField(child=serializers.DictField(), write_only=True)
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        exclude = ("created_at", "updated_at", "status", "total_amount")

    def create(self, validated_data):
        product_quantities = validated_data.pop("product_quantities", [])
        orders_objects = []

        order = Order.objects.create(**validated_data)
        logger.info(f"Заказ с ID {order.id} успешно создан")

        for product in product_quantities:
            product_id = product.get("product_id")
            quantity = product.get("quantity", 1)
            size = product.get("size")

            if product_id is not None and quantity is not None:
                try:
                    product = Product.objects.get(pk=product_id)
                    orders_objects.append(OrderItem(
                        product=product,
                        order=order,
                        quantity=quantity,
                        subtotal=quantity * product.get_current_price(),
                        size=size,
                    ))
                except ObjectDoesNotExist:
                    logger.warning(f"Товара с ID {product_id} не существует")

        OrderItem.objects.bulk_create(orders_objects)

        order.update_total_amount()
        return order

