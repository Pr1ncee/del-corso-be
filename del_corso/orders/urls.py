from django.urls import path, include
from rest_framework.routers import DefaultRouter

from orders import views


app_name = "orders"

router = DefaultRouter()
router.register(r'orders', views.OrderViewSet, basename="orders")

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += router.urls
