import os

from dotenv import load_dotenv

load_dotenv()


class PostgresConfig:
    HOST = os.getenv("POSTGRES_HOST", "localhost")
    PWD = os.getenv("POSTGRES_PASSWORD", "postgres")
    USER = os.getenv("POSTGRES_USER", "postgres")
    NAME = os.getenv("POSTGRES_NAME", "del_corso")
    PORT = os.getenv("POSTGRES_PORT", "5432")
    TEST_NAME = os.getenv("POSTGRES_TEST_DB", "test_del_corso")


class GeneralConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "")
    DOMAIN_NAME = os.getenv("DOMAIN_NAME")
    CACHE_TIMEOUT_SECONDS = int(os.getenv("CACHE_TIMEOUT_SECONDS", 300))
    ENV = os.getenv("ENV", "dev")
    LANGUAGE_CODE = "ru"
    TIME_ZONE = "Europe/Moscow"
    TARGET_IMAGE_DIR = "product_images/"


class AdminConfig:
    USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    EMAIL = os.getenv("ADMIN_EMAIL", "admin@admin.com")
    PWD = os.getenv("ADMIN_PWD", "admin")


class EmailConfig:
    EMAIL_HOST = os.getenv("EMAIL_HOST")
    EMAIL_PORT = os.getenv("EMAIL_PORT")
    EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS")
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
    EMAIL_RECIPIENT_HOST = os.getenv("EMAIL_RECIPIENT_HOST")


class CeleryConfig:
    CELERY_MAX_RETRY = os.getenv("CELERY_MAX_RETRY", 3)
    CELERY_RETRY_BACKOFF = os.getenv("CELERY_RETRY_BACKOFF", 60)


class RedisConfig:
    REDIS_BROKER_URL = os.getenv("REDIS_BROKER_URL")


class InstagramConfig:
    INSTAGRAM_ACCOUNT_NAME = os.getenv("INSTAGRAM_ACCOUNT_NAME", "del.corso.minsk")
    INSTAGRAM_MAX_POSTS = int(os.getenv("INSTAGRAM_MAX_POSTS", 5))
    INSTAGRAM_POST_AGE = int(os.getenv("INSTAGRAM_POST_AGE", 48))  # Hours
    INSTAGRAM_TEMPLATE_URL = "https://www.instagram.com/p/{0}/?hl=ru"


general_config = GeneralConfig()
postgres_config = PostgresConfig()
admin_config = AdminConfig()
email_config = EmailConfig()
celery_config = CeleryConfig()
redis_config = RedisConfig()
instagram_config = InstagramConfig()
