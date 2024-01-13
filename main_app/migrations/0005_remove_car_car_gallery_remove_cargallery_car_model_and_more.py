# Generated by Django 4.2.6 on 2023-11-15 12:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_car_body_color_car_body_type_car_brand_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='car_gallery',
        ),
        migrations.RemoveField(
            model_name='cargallery',
            name='car_model',
        ),
        migrations.AddField(
            model_name='cargallery',
            name='car',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='main_app.car'),
        ),
    ]