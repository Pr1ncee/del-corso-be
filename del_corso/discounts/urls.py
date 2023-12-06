from django.urls import path, include
from rest_framework import routers

from discounts import views


app_name = 'discount'

router = routers.DefaultRouter()
router.register(r'discounted-products', views.DiscountViewSet, basename='discounted-products')


urlpatterns = [
    path('', include(router.urls))
]

urlpatterns += router.urls
