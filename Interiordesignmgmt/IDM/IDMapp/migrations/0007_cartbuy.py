# Generated by Django 5.0.2 on 2024-03-22 07:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IDMapp', '0006_remove_productbuy_items_productbuy_product_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartBuy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('name', models.CharField(max_length=200)),
                ('apartment', models.CharField(max_length=200)),
                ('place', models.CharField(max_length=200)),
                ('pincode', models.IntegerField()),
                ('phone_number', models.BigIntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IDMapp.cart')),
                ('user', models.ForeignKey(limit_choices_to={'user_type': 'Customer'}, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
