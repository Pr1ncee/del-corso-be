from rest_framework import serializers

from banners.models import BannerImage


class BannerImageSerializer(serializers.ModelSerializer):
    image_path = serializers.SerializerMethodField()

    def get_image_path(self, obj):
        image_path = obj.image.path.split("/")[-1]
        return image_path

    class Meta:
        model = BannerImage
        fields = ("image_path", "main", "popular_categories")
