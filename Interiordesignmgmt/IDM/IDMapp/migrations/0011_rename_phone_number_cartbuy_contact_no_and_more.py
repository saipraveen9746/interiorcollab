# Generated by Django 5.0.2 on 2024-03-26 09:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IDMapp', '0010_agentproductbooking_agent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartbuy',
            old_name='phone_number',
            new_name='contact_no',
        ),
        migrations.RemoveField(
            model_name='cartbuy',
            name='product',
        ),
        migrations.AddField(
            model_name='cartbuy',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='cartbuy',
            name='items',
            field=models.ManyToManyField(related_name='cart_buys', to='IDMapp.cartitem'),
        ),
        migrations.AlterField(
            model_name='cartbuy',
            name='apartment',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='cartbuy',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='cartbuy',
            name='place',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='cartbuy',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='cartbuy',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_buys', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='CartBuyItem',
        ),
    ]