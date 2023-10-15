from django.db.models import Q
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from store.serializers import (
    SizeSerializer,
    ColorSerializer,
    TypeCategorySerializer,
    SeasonCategorySerializer,
    ProductSizeSerializer,
)
from store.models import (
    Size,
    Color,
    TypeCategory,
    SeasonCategory,
    Product,
    ProductSize,
)


class SizeViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = SizeSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')

        if not pk:
            return Size.objects.all()

        return Size.objects.filter(pk=pk)


class ColorViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    serializer_class = ColorSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if not pk:
            return Color.objects.all()

        return Color.objects.filter(pk=pk)


class TypeCategoryViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = TypeCategorySerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if not pk:
            return TypeCategory.objects.all()

        return TypeCategory.objects.filter(pk=pk)

    @action(detail=False, methods=["GET"], url_path="popular-categories")
    def popular_categories(self, request):
        popular_categories = TypeCategory.objects.filter(is_popular=True)
        serializer = self.get_serializer(popular_categories, many=True)
        return Response(serializer.data)


class SeasonCategoryViewSet(mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):
    serializer_class = SeasonCategorySerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if not pk:
            return SeasonCategory.objects.all()

        return SeasonCategory.objects.filter(pk=pk)


class ProductViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = ProductSizeSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = ProductSize.objects.all()

        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')

        if min_price:
            queryset = queryset.filter(product__price__gte=float(min_price))
        if max_price:
            queryset = queryset.filter(product__price__lte=float(max_price))

        sizes = self.request.GET.getlist('size')
        if sizes:
            size_filters = Q()
            for size in sizes:
                size_filters |= Q(sizes__size=int(size))
            queryset = queryset.filter(size_filters)

        product_types = self.request.GET.getlist('type')
        if product_types:
            type_filters = Q()
            for product_type in product_types:
                type_filters |= Q(product__type_category__name=product_type)
            queryset = queryset.filter(type_filters)

        colors = self.request.GET.getlist('color')
        if colors:
            color_filters = Q()
            for color in colors:
                color_filters |= Q(product__color__color=color)
            queryset = queryset.filter(color_filters)

        seasons = self.request.GET.getlist('season')
        if seasons:
            season_filters = Q()
            for season in seasons:
                season_filters |= Q(product__season_category__name=season)
            queryset = queryset.filter(season_filters)

        return queryset.distinct()

    @action(detail=True, methods=["GET"], url_path="type-category")
    def get_products_by_type_category(self, request, pk: int = None):
        type_category = self.get_object()
        products = Product.objects.filter(type_category__id=type_category.id)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"], url_path="new-collection")
    def get_new_collection_products(self, request):
        new_collection_products = Product.objects.filter(new_collection=True)
        serializer = self.get_serializer(new_collection_products, many=True)
        return Response(serializer.data)
