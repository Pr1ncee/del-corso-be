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

    def get_image_paths(self, obj):
        product_images = obj.productimage_set.all()
        image_paths = [image.image.path for image in product_images]
        return image_paths

    class Meta:
        model = Product
        exclude = ("created_at", "updated_at")
