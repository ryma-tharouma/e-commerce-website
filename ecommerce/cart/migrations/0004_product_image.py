# Generated by Django 4.2.7 on 2025-04-09 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_remove_cartitem_user_cartitem_session_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
    ]
