# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-30 13:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_commentqa_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentqa',
            name='subject',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='subject',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
