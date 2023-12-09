from pathlib import Path

from del_corso.config import postgres_config, general_config, email_config, redis_config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = general_config.SECRET_KEY

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

if (env := general_config.ENV.lower()) == "prod":
    DEBUG = False
    ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
elif env == "dev":
    DEBUG = True
    ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http"
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'http')
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

# Application definition
INSTALLED_APPS = [
    # Style
    "jazzmin",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party(external)
    "rest_framework",
    "colorfield",

    # Custom(internal)
    "authorization",
    "discounts",
    "orders",
    "store",
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.cache.FetchFromCacheMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = "del_corso.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "del_corso.wsgi.application"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': postgres_config.NAME,
        'USER': postgres_config.USER,
        'PASSWORD': postgres_config.PWD,
        'HOST': postgres_config.HOST,
        'PORT': postgres_config.PORT,
        'TEST': {
            'NAME': postgres_config.TEST_NAME,
        }
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": redis_config.REDIS_BROKER_URL,
    }
}

CACHE_MIDDLEWARE_ALIAS = "default"
CACHE_MIDDLEWARE_SECONDS = general_config.CACHE_TIMEOUT_SECONDS  # Seconds
CACHE_MIDDLEWARE_KEY_PREFIX = ""

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = general_config.LANGUAGE_CODE

TIME_ZONE = general_config.TIME_ZONE

USE_I18N = True

USE_TZ = True

USE_L10N = True

STATIC_URL = "/static/"

STATICFILES_DIRS = [BASE_DIR / "static"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 36
}

JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "Del Corso Admin",

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "Del Corso",

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "Del Corso",

    "site_logo": "store/img/dc_logo.jpg",

    "show_ui_builder": True,

    # Welcome text on the login screen
    "welcome_sign": "Добро пожаловать в админ-панель Del Corso",

    # Copyright on the footer
    "copyright": "Del Corso",

    "search_model": ["store.Product", "orders.Order", "discounts.Discount", "discounts.ProductDiscount"],

    ############
    # Top Menu #
    ############

    # Links to put along the top menu
    "topmenu_links": [

        # Url that gets reversed (Permissions can be added)
        {"name": "Главная",  "url": "admin:index", "permissions": ["auth.view_user"]},

        {"app": "auth"},

        # App with dropdown menu to all its models pages (Permissions checked against models)
        {"app": "store"},
    ],

    #############
    # User Menu #
    #############

    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    "usermenu_links": [
        {"model": "auth.user"}
    ],

    #############
    # Side Menu #
    #############

    # Whether to display the side menu
    "show_sidebar": True,

    # Whether to aut expand the menu
    "navigation_expanded": True,

    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": ["auth"],

    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = email_config.EMAIL_HOST
EMAIL_PORT = email_config.EMAIL_PORT
EMAIL_USE_TLS = email_config.EMAIL_USE_TLS
EMAIL_HOST_USER = email_config.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = email_config.EMAIL_HOST_PASSWORD

CELERY_BROKER_URL = redis_config.REDIS_BROKER_URL
CELERY_TIMEZONE = general_config.TIME_ZONE
