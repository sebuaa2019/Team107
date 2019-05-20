# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-05-19 17:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0015_auto_20190519_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scene',
            name='control_service_id',
            field=models.IntegerField(default=0, verbose_name='控制服务id'),
        ),
        migrations.AlterField(
            model_name='scene',
            name='read_service_id',
            field=models.IntegerField(default=0, verbose_name='只读服务id'),
        ),
        migrations.AlterField(
            model_name='scene',
            name='trigger_condition',
            field=models.IntegerField(default=0, verbose_name='触发条件'),
        ),
        migrations.AlterField(
            model_name='scene',
            name='trigger_value',
            field=models.FloatField(default=0.0, verbose_name='触发值'),
        ),
    ]