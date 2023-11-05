from django.contrib import admin
from django.urls import path, include
from rest_framework import routers


routers = routers.DefaultRouter()
urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/v1/', include('store.urls')),
    path('api/v1/', include('orders.urls')),
    path('api/v1/', include('discounts.urls')),
    path('api/v1/', include('instagram.urls')),
]

urlpatterns += routers.urls
