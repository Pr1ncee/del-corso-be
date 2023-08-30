from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from del_corso.config import admin_config


class Command(BaseCommand):
    """
    Create an admin user with the creds from .env file. Must be called only with 'manage.py'
    """
    def handle(self, *args, **options):
        user_queryset = User.objects

        username = admin_config.USERNAME
        email = admin_config.EMAIL
        password = admin_config.PWD

        try:
            self.stdout.write(f'Creating account for {username} {email}')
            admin = user_queryset.create_superuser(email=email, username=username, password=password)
            admin.is_active = True
            admin.is_superuser = True
        except IntegrityError:
            self.stdout.write('Admin account with such credentials already exists')
        else:
            admin.save()
            self.stdout.write('Created successfully')
