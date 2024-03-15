# Generated by Django 5.0.2 on 2024-03-14 07:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IDMapp', '0002_alter_officebookdesign_contact_no'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeBookDesign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('email', models.TextField(max_length=10000, null=True)),
                ('contact_no', models.BigIntegerField(null=True)),
                ('address', models.TextField(null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IDMapp.home')),
                ('user', models.ForeignKey(limit_choices_to={'user_type': 'Customer'}, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]