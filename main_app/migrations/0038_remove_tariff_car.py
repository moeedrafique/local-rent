# Generated by Django 4.2.6 on 2024-01-13 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0037_alter_tariff_car'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tariff',
            name='car',
        ),
    ]
