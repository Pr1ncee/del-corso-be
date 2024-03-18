from rest_framework import mixins, viewsets

from banners.models import BannerImage
from banners.serializers import BannerImageSerializer


class BannerViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = BannerImageSerializer

    def get_queryset(self):
        return BannerImage.objects.all()
