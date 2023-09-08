from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from store.serializers import (
    SizeSerializer,
    ColorSerializer,
    TypeCategorySerializer,
    SeasonCategorySerializer,
    ProductSerializer
)
from store.models import (
    Size,
    Color,
    TypeCategory,
    SeasonCategory,
    Product
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
    serializer_class = ProductSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if not pk:
            return Product.objects.all()

        return Product.objects.filter(pk=pk)

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
