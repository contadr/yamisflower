# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-22 15:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20170822_1543'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='flower',
            options={'ordering': ['-id']},
        ),
        migrations.AddField(
            model_name='flower',
            name='thumbnail',
            field=models.ImageField(blank=True, upload_to='flower/thumbnail'),
        ),
        migrations.AlterField(
            model_name='floimg',
            name='file',
            field=models.FileField(upload_to='flower/galleries', verbose_name='FloImg'),
        ),
    ]