# Generated by Django 3.1.6 on 2021-11-29 17:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0006_auto_20211129_2052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenses',
            name='date',
            field=models.DateField(default=datetime.date(2021, 11, 29), verbose_name='Дата'),
        ),
    ]
