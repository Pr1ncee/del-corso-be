from rest_framework import viewsets, status
from rest_framework.response import Response

from orders.serializers import OrderSerializer


class OrderViewSet(viewsets.GenericViewSet):
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
