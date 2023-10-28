from datetime import datetime
from smtplib import SMTPException
from sys import exc_info

import pytz
from django.core.mail import send_mail

from del_corso.config import general_config, email_config


def send_new_order_notification_email(new_order_id: int) -> None:
    current_time = datetime.now(pytz.timezone(general_config.TIME_ZONE)).strftime("%Y-%m-%d %H:%M")
    subject = f"""Оформлен новый заказ. Время: {current_time}"""
    message = f"""
        Сделан новый заказа под номером {new_order_id}. 
        Ознакомиться можно по ссылке: https://{general_config.DOMAIN_NAME}:8000/admin/orders/order/
    """

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=email_config.EMAIL_HOST_USER,
            recipient_list=[email_config.EMAIL_RECIPIENT_HOST],
            fail_silently=False,
        )
    except SMTPException:
        print(str(exc_info()[1]))
