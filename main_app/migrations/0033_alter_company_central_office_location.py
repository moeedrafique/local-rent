# Generated by Django 4.2.6 on 2024-01-05 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0032_alter_carextras_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='central_office_location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
