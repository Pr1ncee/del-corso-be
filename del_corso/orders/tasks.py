import logging
from datetime import datetime
from smtplib import SMTPException
from sys import exc_info

from django.core.mail import send_mail
from del_corso.celery import app
import pytz

from del_corso import setup_logging
from del_corso.config import general_config, email_config, celery_config

setup_logging()
logger = logging.getLogger(__name__)


@app.task(max_retries=celery_config.CELERY_MAX_RETRY, retry_backoff=celery_config.CELERY_RETRY_BACKOFF)
def send_new_order_notification_email(new_order_id: int) -> None:
    current_time = datetime.now(pytz.timezone(general_config.TIME_ZONE)).strftime("%Y-%m-%d %H:%M")
    subject = f"""Оформлен новый заказ. Время: {current_time}"""
    message = f"""
        Сделан новый заказа под номером {new_order_id}. 
        Ознакомиться можно по ссылке: https://{general_config.DOMAIN_NAME}:8000/admin/orders/order/
    """

    try:
        logger.info(f"New Order ({new_order_id}) created. Sending email notification...")
        send_mail(
            subject=subject,
            message=message,
            from_email=email_config.EMAIL_HOST_USER,
            recipient_list=[email_config.EMAIL_RECIPIENT_HOST],
            fail_silently=False,
        )
        logger.info("Email notification was sent successfully!")
    except SMTPException as e:
        raise e
        logger.info(f"Failed to send the email notification. The following error occurred: {str(exc_info()[1])}")
