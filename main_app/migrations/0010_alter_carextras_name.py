# Generated by Django 4.2.6 on 2023-11-15 20:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_extras_alter_carextras_maximum_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carextras',
            name='name',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='car_extras', to='main_app.extras'),
        ),
    ]