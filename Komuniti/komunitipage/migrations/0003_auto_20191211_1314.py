# Generated by Django 2.2.6 on 2019-12-11 13:14

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('komunitipage', '0002_auto_20191207_1216'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='description',
        ),
        migrations.RemoveField(
            model_name='post',
            name='title',
        ),
        migrations.AlterField(
            model_name='community',
            name='date_pub',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='community',
            name='tags',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}),
        ),
    ]