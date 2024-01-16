from rest_framework import serializers

from store.serializers import ProductSerializer
from discounts.models import Discount, ProductDiscount


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        exclude = ("created_at", "updated_at")


class ProductDiscountSerializer(serializers.ModelSerializer):
    discount = DiscountSerializer()

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        first_product = instance.products.first()
        representation['product'] = ProductSerializer(first_product).data if first_product else None
        return representation

    class Meta:
        model = ProductDiscount
        exclude = ("created_at", "updated_at")
