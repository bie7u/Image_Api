# Generated by Django 4.0.5 on 2022-06-23 00:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_alter_imgthumbnail_image_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timegenerateimg',
            name='time_of_expiry',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(300), django.core.validators.MaxValueValidator(30000)]),
        ),
    ]
