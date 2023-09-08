from django.urls import path, include
from rest_framework import routers

from store import views


app_name = 'store'

router = routers.DefaultRouter()
router.register(r'size', views.SizeViewSet, basename='size')
router.register(r'color', views.ColorViewSet, basename='color')
router.register(r'type-category', views.TypeCategoryViewSet, basename='type_category')
router.register(r'season', views.SeasonCategoryViewSet, basename='season')
router.register(r'product', views.ProductViewSet, basename='product')


urlpatterns = [
    path('', include(router.urls))
]

urlpatterns += router.urls
