# Generated by Django 4.2.2 on 2025-04-27 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0009_product_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_id_delivery',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
