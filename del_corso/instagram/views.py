from rest_framework import viewsets
from rest_framework.response import Response

from instagram.services import get_latest_account_posts
from del_corso.config import instagram_config


class PostViewSet(viewsets.ViewSet):
    def list(self, request):
        response, status_code = get_latest_account_posts(
            account_name=instagram_config.INSTAGRAM_ACCOUNT_NAME,
            max_posts=instagram_config.INSTAGRAM_MAX_POSTS
        )
        return Response(data=response, status=status_code)
