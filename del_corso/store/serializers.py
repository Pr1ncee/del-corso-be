from django.apps import apps
from django.utils import timezone
from rest_framework import serializers

from store.enums.material_enum import (
    TrueToSizeType,
    UpperMaterialType,
    LiningMaterialType,
    CompletenessType
)
from store.models import (
    Size,
    Color,
    TypeCategory,
    SeasonCategory,
    Product,
    ProductImage,
    ProductSize
)


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


class BaseProductSerialzer(serializers.ModelSerializer):
    color = ColorSerializer()
    season_categories = serializers.SerializerMethodField()
    type_category = TypeCategorySerializer()
    image_paths = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()
    true_to_size = serializers.SerializerMethodField()
    completeness = serializers.SerializerMethodField()
    upper_material = serializers.SerializerMethodField()
    lining_material = serializers.SerializerMethodField()

    def get_completeness(self, obj):
        return CompletenessType.get_description(obj.completeness)

    def get_lining_material(self, obj):
        return LiningMaterialType.get_description(obj.lining_material)

    def get_upper_material(self, obj):
        return UpperMaterialType.get_description(obj.upper_material)

    def get_true_to_size(self, obj):
        return TrueToSizeType.get_description(obj.true_to_size)

    def get_season_categories(self, obj):
        return [season.name for season in obj.season_category.all()]

    def get_image_paths(self, obj):
        product_images = obj.productimage_set.all()
        image_paths = [image.image.path.split("/")[-1] for image in product_images]
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

        return {}


class ProductSerializer(BaseProductSerialzer):
    class Meta:
        model = Product
        exclude = ("created_at", "updated_at")


class ProductSizeSerializer(serializers.ModelSerializer):
    sizes = serializers.SerializerMethodField()
    product = ProductSerializer()

    def get_sizes(self, obj):
        sizes = obj.sizes.all().values_list("size", flat=True)
        return sizes

    class Meta:
        model = ProductSize
        fields = '__all__'


class ProductDetailedSerializer(BaseProductSerialzer):
    sizes = serializers.SerializerMethodField()

    def get_sizes(self, obj):
        raw_sizes = ProductSize.objects.get(product__name=obj.name)
        return raw_sizes.sizes.all().values_list("size", flat=True)

    class Meta:
        model = Product
        exclude = ("created_at", "updated_at")

