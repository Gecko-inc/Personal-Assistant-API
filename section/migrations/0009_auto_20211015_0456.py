# Generated by Django 3.1.6 on 2021-10-15 01:56

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('section', '0008_articlemedia_rich_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlemedia',
            name='rich_text',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, default=' '),
        ),
    ]
