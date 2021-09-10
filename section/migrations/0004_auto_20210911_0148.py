# Generated by Django 3.1.6 on 2021-09-10 22:48

import config.views
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('section', '0003_section_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-sort'], 'verbose_name': 'Статья', 'verbose_name_plural': 'Статьи'},
        ),
        migrations.AlterModelOptions(
            name='articlemedia',
            options={'ordering': ['-sort'], 'verbose_name': 'Текст', 'verbose_name_plural': 'Тексты'},
        ),
        migrations.AlterModelOptions(
            name='section',
            options={'ordering': ['-sort'], 'verbose_name': 'Раздел', 'verbose_name_plural': 'Разделы'},
        ),
        migrations.RemoveField(
            model_name='article',
            name='image',
        ),
        migrations.RemoveField(
            model_name='article',
            name='short_description',
        ),
        migrations.RemoveField(
            model_name='article',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='article',
            name='text',
        ),
        migrations.RemoveField(
            model_name='articlemedia',
            name='title',
        ),
        migrations.RemoveField(
            model_name='section',
            name='description',
        ),
        migrations.RemoveField(
            model_name='section',
            name='image',
        ),
        migrations.RemoveField(
            model_name='section',
            name='show_main',
        ),
        migrations.RemoveField(
            model_name='section',
            name='slug',
        ),
        migrations.AddField(
            model_name='article',
            name='sort',
            field=models.IntegerField(default=0, verbose_name='Сортировка'),
        ),
        migrations.AddField(
            model_name='articlemedia',
            name='sort',
            field=models.IntegerField(default=0, verbose_name='Сортировка'),
        ),
        migrations.AddField(
            model_name='articlemedia',
            name='text',
            field=models.TextField(null=True, verbose_name='Текст'),
        ),
        migrations.AddField(
            model_name='section',
            name='sort',
            field=models.IntegerField(default=0, verbose_name='Сортировка'),
        ),
        migrations.AlterField(
            model_name='articlemedia',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detail', to='section.article', verbose_name='Статья'),
        ),
        migrations.AlterField(
            model_name='articlemedia',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=config.views.get_upload_to, verbose_name='Изображение'),
        ),
    ]