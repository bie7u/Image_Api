# Generated by Django 4.0.5 on 2022-06-13 07:11

import core.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_remove_imgupload_image_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeGenerateImg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to=core.models.image_file_path)),
                ('image_type', models.CharField(blank=True, choices=[(1, 'original'), (2, '200px'), (3, '400px')], default=1, max_length=255, null=True)),
                ('time_of_expiry', models.IntegerField(validators=[django.core.validators.MinValueValidator(300), django.core.validators.MaxValueValidator(30000)])),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('original_image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.imgupload')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]