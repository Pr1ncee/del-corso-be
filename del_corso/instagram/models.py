from django.db import models

from base_models import BaseModel


class Post(BaseModel):
    latest_posts = models.JSONField(default=list)
