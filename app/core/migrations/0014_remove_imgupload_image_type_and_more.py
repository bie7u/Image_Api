# Generated by Django 4.0.5 on 2022-06-12 21:18

import core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_imgupload_original_image_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imgupload',
            name='image_type',
        ),
        migrations.RemoveField(
            model_name='imgupload',
            name='original_image_id',
        ),
        migrations.CreateModel(
            name='ImgThumbnail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to=core.models.image_file_path)),
                ('image_type', models.CharField(blank=True, choices=[(1, 'original'), (2, '200px'), (3, '400px')], default=1, max_length=255, null=True)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('original_image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.imgupload')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
