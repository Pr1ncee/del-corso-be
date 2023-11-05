from datetime import timedelta

from django.utils import timezone
from rest_framework import status

from del_corso.config import instagram_config
from instagram.models import Post
from instaloader import Instaloader, Profile


def get_latest_account_posts(account_name: str, max_posts: int) -> tuple[list[tuple], int] | tuple[dict[str], int]:
    posts = Post.objects.all()
    if not posts:
        data, status_code = load_instagram_posts(account_name, max_posts)
        if status_code == status.HTTP_200_OK:
            Post.objects.create(latest_posts=data)
        return data, status_code

    latest_posts = posts.first()
    if not latest_posts_updated_recently(latest_posts):
        data, status_code = load_instagram_posts(account_name, max_posts)
        if status_code == status.HTTP_200_OK:
            latest_posts.latest_posts = data
            latest_posts.save()
        return data, status_code

    return latest_posts.latest_posts, status.HTTP_200_OK


def latest_posts_updated_recently(latest_posts: Post) -> bool:
    current_time = timezone.now()
    post_age = current_time - timedelta(hours=instagram_config.INSTAGRAM_POST_AGE)
    return latest_posts.updated_at >= post_age


def load_instagram_posts(account_name: str, max_posts: int) -> tuple[list[tuple], int] | tuple[dict[str], int]:
    try:
        loader = Instaloader()
        profile = Profile.from_username(loader.context, account_name)
        posts = []

        for post in profile.get_posts():
            if len(posts) >= max_posts:
                break

            post_shortcode = post.shortcode
            post_url = instagram_config.INSTAGRAM_TEMPLATE_URL.format(post_shortcode)
            image_url = post.url
            posts.append((post_url, image_url))

        return posts, status.HTTP_200_OK

    except Exception as e:
        return {'error': str(e)}, status.HTTP_400_BAD_REQUEST
