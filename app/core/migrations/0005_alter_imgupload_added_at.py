# Generated by Django 4.0.5 on 2022-06-10 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_rename_date_imgupload_added_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imgupload',
            name='added_at',
            field=models.DateTimeField(),
        ),
    ]
