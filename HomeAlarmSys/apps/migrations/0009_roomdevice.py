# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-05-11 15:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0008_auto_20190506_2137'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_id', models.IntegerField(verbose_name='房间id')),
                ('device_id', models.IntegerField(verbose_name='设备id')),
            ],
            options={
                'verbose_name': '房间设备分配表',
                'verbose_name_plural': '房间设备分配表',
            },
        ),
    ]