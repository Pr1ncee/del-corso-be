from django.urls import path, include
from rest_framework import routers

from instagram import views


app_name = 'instagram'

router = routers.DefaultRouter()
router.register(r'get-latest-posts', views.PostViewSet, basename='get-latest-posts')


urlpatterns = [
    path('', include(router.urls))
]

urlpatterns += router.urls
