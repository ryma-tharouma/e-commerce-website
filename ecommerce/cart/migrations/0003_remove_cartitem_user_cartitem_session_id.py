# Generated by Django 4.2.7 on 2025-03-15 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_cartitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='user',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='session_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
