# Generated by Django 2.2.1 on 2019-12-11 16:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_auto_20191211_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citydict',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='courseorg',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间'),
        ),
    ]
