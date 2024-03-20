# Generated by Django 5.0.2 on 2024-03-19 11:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IDMapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListWish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IDMapp.product')),
                ('user', models.ForeignKey(limit_choices_to={'user_type': 'Customer'}, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]