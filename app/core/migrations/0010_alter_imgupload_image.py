# Generated by Django 4.0.5 on 2022-06-12 19:08

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_remove_imgupload_name_imgupload_image_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imgupload',
            name='image',
            field=models.ImageField(height_field='200', null=True, upload_to=core.models.image_file_path),
        ),
    ]