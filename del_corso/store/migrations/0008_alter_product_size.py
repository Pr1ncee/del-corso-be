# Generated by Django 4.2.4 on 2023-10-23 09:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_product_in_stock_product_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.size', verbose_name='Размер'),
        ),
    ]
