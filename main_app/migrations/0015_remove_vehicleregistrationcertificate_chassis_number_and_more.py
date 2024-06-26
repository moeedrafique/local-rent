# Generated by Django 4.2.6 on 2023-11-17 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0014_alter_carfeatures_airbags_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehicleregistrationcertificate',
            name='chassis_number',
        ),
        migrations.RemoveField(
            model_name='vehicleregistrationcertificate',
            name='engine_number',
        ),
        migrations.RemoveField(
            model_name='vehicleregistrationcertificate',
            name='owner_address',
        ),
        migrations.RemoveField(
            model_name='vehicleregistrationcertificate',
            name='owner_name',
        ),
        migrations.RemoveField(
            model_name='vehicleregistrationcertificate',
            name='registration_date',
        ),
        migrations.RemoveField(
            model_name='vehicleregistrationcertificate',
            name='registration_number',
        ),
        migrations.AddField(
            model_name='vehicleregistrationcertificate',
            name='image',
            field=models.ImageField(default=None, upload_to='vehicle_registration_certificate/'),
        ),
    ]
