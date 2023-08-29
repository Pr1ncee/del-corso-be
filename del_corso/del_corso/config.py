import os

from dotenv import load_dotenv

load_dotenv()


class PostgresConfig:
    HOST = os.getenv("POSTGRES_HOST", "localhost")
    PWD = os.getenv("POSTGRES_PASSWORD", "postgres")
    USER = os.getenv("POSTGRES_USER", "postgres")
    NAME = os.getenv("POSTGRES_NAME", "del_corso")
    PORT = os.getenv("POSTGRES_PORT", "5432")


class GeneralConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "")
    DEBUG = True
    LANGUAGE_CODE = "ru"
    TIME_ZONE = "Europe/Moscow"


general_config = GeneralConfig()
postgres_config = PostgresConfig()
