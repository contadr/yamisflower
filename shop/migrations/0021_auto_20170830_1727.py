# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-30 17:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0020_auto_20170830_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentqa',
            name='subject',
            field=models.CharField(choices=[('상품문의', '상품문의'), ('배송문의', '배송문의'), ('입금문의', '입금문의'), ('기타문의', '기타문의')], max_length=50, verbose_name='문의유형'),
        ),
    ]
