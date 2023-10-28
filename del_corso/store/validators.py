import logging
import re

from django.core.exceptions import ValidationError

from del_corso import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


def validate_phone_number(value):
    pattern = r'^\+\d{12}$'
    if not re.match(pattern, value):
        logger.info(f"Input phone number is invalid! ({value})")
        raise ValidationError('Введите действительный номер телефона в формате: +375291235678.')
