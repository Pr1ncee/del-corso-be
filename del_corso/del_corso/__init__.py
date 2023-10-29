from del_corso.celery import app as celery_app
from del_corso.logging import setup_logging

__all__ = ("celery_app", "setup_logging")
