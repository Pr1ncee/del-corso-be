from django.apps import apps
from django.utils import timezone
from rest_framework import serializers

from store.models import Size, Color, TypeCategory, SeasonCategory, Product, ProductImage


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        exclude = ("created_at", "updated_at")


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        exclude = ("created_at", "updated_at")


class SeasonCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SeasonCategory
        exclude = ("created_at", "updated_at")


class TypeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeCategory
        exclude = ("created_at", "updated_at")


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("image",)


class ProductSerializer(serializers.ModelSerializer):
    size = SizeSerializer()
    color = ColorSerializer()
    season_category = SeasonCategorySerializer()
    type_category = TypeCategorySerializer()
    image_paths = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()

    def get_image_paths(self, obj):
        product_images = obj.productimage_set.all()
        image_paths = [image.image.path for image in product_images]
        return image_paths

    def get_discount(self, obj):
        product_discount_model = apps.get_model('discounts', 'ProductDiscount')
        active_discount = product_discount_model.objects.filter(
            product=obj,
            discount__start_date__lte=timezone.now().date(),
            discount__end_date__gte=timezone.now().date()
        ).first()

        if active_discount:
            return {
                'discount_price': active_discount.discount.discount_price,
                'start_date': active_discount.discount.start_date,
                'end_date': active_discount.discount.end_date,
            }

        return None

    class Meta:
        model = Product
        exclude = ("created_at", "updated_at")
