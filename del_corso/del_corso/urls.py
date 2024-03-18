from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers


if settings.DEBUG:
    routers = routers.DefaultRouter()
else:
    routers = routers.SimpleRouter()

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/v1/', include('store.urls')),
    path('api/v1/', include('orders.urls')),
    path('api/v1/', include('discounts.urls')),
    path('api/v1/', include('banners.urls')),
]

urlpatterns += routers.urls
