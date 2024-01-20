from rest_framework import serializers

from banners.models import BannerImage
from store.serializers import SeasonCategorySerializer


class BannerImageSerializer(serializers.ModelSerializer):
    image_path = serializers.SerializerMethodField()
    season_category = SeasonCategorySerializer()

    def get_image_path(self, obj):
        image_path = obj.image.path.split("/")[-1]
        return image_path

    class Meta:
        model = BannerImage
        fields = ("image_path", "main", "season_category")
