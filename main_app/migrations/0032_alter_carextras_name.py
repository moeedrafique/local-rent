# Generated by Django 4.2.6 on 2024-01-05 09:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0031_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carextras',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='car_extras', to='main_app.extras'),
        ),
    ]
