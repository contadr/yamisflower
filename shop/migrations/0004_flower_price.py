# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-22 15:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20170822_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='flower',
            name='price',
            field=models.IntegerField(default=0, verbose_name='가격 (원)'),
            preserve_default=False,
        ),
    ]