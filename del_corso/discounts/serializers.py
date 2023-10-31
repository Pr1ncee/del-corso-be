from rest_framework import serializers

from store.serializers import ProductSerializer
from discounts.models import Discount, ProductDiscount


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        exclude = ("created_at", "updated_at")


class ProductDiscountSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    discount = DiscountSerializer()

    class Meta:
        model = ProductDiscount
        exclude = ("created_at", "updated_at")
