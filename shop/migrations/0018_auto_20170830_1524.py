# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-30 15:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0017_auto_20170830_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='content',
            field=models.TextField(verbose_name='내용'),
        ),
        migrations.AlterField(
            model_name='review',
            name='subject',
            field=models.CharField(max_length=50, verbose_name='제목'),
        ),
    ]