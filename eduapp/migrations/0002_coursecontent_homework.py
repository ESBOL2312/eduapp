# Generated by Django 3.1.7 on 2021-06-16 13:22

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eduapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursecontent',
            name='homeWork',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, verbose_name='as'),
        ),
    ]
