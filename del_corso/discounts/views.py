from rest_framework import viewsets, mixins
from rest_framework.pagination import PageNumberPagination

from discounts.models import ProductDiscount
from discounts.serializers import ProductDiscountSerializer


class DiscountViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = ProductDiscountSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if not pk:
            return ProductDiscount.objects.all()

        return ProductDiscount.objects.filter(pk=pk)
