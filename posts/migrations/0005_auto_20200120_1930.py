# Generated by Django 3.0.2 on 2020-01-20 16:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20200120_1926'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='slug',
        ),
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(blank=True, verbose_name=datetime.datetime(2020, 1, 20, 19, 30, 30, 556975)),
        ),
    ]
