from django.urls import path, include
from rest_framework import routers

from banners import views


app_name = 'banners'

router = routers.DefaultRouter()
router.register(r'banners', views.BannerViewSet, basename='banners')

urlpatterns = [
    path('', include(router.urls))
]

urlpatterns += router.urls
