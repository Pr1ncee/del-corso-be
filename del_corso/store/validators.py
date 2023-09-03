import re

from django.core.exceptions import ValidationError


def validate_phone_number(value):
    pattern = r'^\+\d{12}$'
    if not re.match(pattern, value):
        raise ValidationError('Введите действительный номер телефона в формате: +375-(29)-123-56-78.')
