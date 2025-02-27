# Generated by Django 4.2.4 on 2023-12-06 16:27

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import store.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата последнего изменения')),
                ('first_name', models.CharField(max_length=100, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=100, verbose_name='Фамилия')),
                ('surname', models.CharField(max_length=100, verbose_name='Отчество')),
                ('country', models.CharField(max_length=50, verbose_name='Страна')),
                ('telephone_number', models.CharField(max_length=20, validators=[store.validators.validate_phone_number], verbose_name='Номер телефона')),
                ('email', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator(message='Введите действительный адрес электронной почты.')], verbose_name='Электронный адрес')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий к заказу')),
                ('address', models.TextField(verbose_name='Адрес')),
                ('order_date', models.DateField(verbose_name='Дата заказа')),
                ('total_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Цена заказа')),
                ('status', models.CharField(choices=[('Pending', 'В ожидании обработки'), ('Processing', 'Обрабатывается'), ('Shipped', 'Передан курьеру'), ('Delivered', 'Доставлен'), ('Canceled', 'Отменен')], default='Pending', max_length=50, verbose_name='Статус')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата последнего изменения')),
                ('quantity', models.PositiveIntegerField(verbose_name='Количество')),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Итоговая сумма')),
                ('size', models.IntegerField(null=True, verbose_name='Размер')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order', verbose_name='Заказ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Позиция заказа',
                'verbose_name_plural': 'Позиции заказов',
            },
        ),
    ]
