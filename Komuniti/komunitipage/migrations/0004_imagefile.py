# Generated by Django 2.2.6 on 2019-12-17 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('komunitipage', '0003_auto_20191211_1314'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload', models.FileField(upload_to='gallery')),
                ('url', models.TextField(blank=True)),
            ],
        ),
    ]