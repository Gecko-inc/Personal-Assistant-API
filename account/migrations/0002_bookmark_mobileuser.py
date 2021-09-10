# Generated by Django 3.1.6 on 2021-09-10 22:48

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('section', '0004_auto_20210911_0148'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MobileUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=130, unique=True, verbose_name='Токен')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата регистрации')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи мобильного приложения',
            },
        ),
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='section.article')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarks', to='account.mobileuser')),
            ],
            options={
                'verbose_name': 'Закладка',
                'verbose_name_plural': 'Закладки',
            },
        ),
    ]