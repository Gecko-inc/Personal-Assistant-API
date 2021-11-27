# Generated by Django 3.1.6 on 2021-11-27 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_user_step_target'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='balance',
            field=models.FloatField(default=0.0, verbose_name='Баланс'),
        ),
        migrations.AlterField(
            model_name='user',
            name='money_limit',
            field=models.FloatField(default=30000.0, verbose_name='Денежный лимит'),
        ),
    ]
