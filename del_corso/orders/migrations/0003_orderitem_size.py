# Generated by Django 4.2.4 on 2023-10-22 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='size',
            field=models.IntegerField(null=True, verbose_name='Размер'),
        ),
    ]
