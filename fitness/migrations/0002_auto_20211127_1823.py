# Generated by Django 3.1.6 on 2021-11-27 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfitness',
            name='progress',
            field=models.PositiveIntegerField(blank=True, verbose_name='Прогресс упражнения'),
        ),
    ]