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
        product_type = self.request.GET.get('type')

        if not pk:
            if product_type:
                return ProductDiscount.objects.filter(product__type_category__name=product_type)
            else:
                return ProductDiscount.objects.all()

        return ProductDiscount.objects.filter(pk=pk)
