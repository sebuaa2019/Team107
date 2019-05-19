from django.db import models
from django.contrib.auth.models import AbstractUser
import json


class User(models.Model):
    name = models.CharField(verbose_name="昵称", max_length=20)
    password = models.CharField(verbose_name="密码", max_length=257)
    email = models.EmailField(verbose_name="邮箱")
    phone = models.CharField(verbose_name="手机", max_length=20)
    role = models.PositiveSmallIntegerField(verbose_name="角色", choices=((1, '普通用户'), (2, '管理员'), (3, '超级管理员')),
                                            default=1)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name


class Room(models.Model):
    room_name = models.CharField(verbose_name="房间名称", max_length=20)

    def __str__(self):
        return {"id": self.id, "room_name": self.room_name}

    class Meta:
        verbose_name = "房间"
        verbose_name_plural = verbose_name


class Device(models.Model):
    device_id = models.IntegerField(verbose_name="设备id", primary_key=True)
    device_name = models.CharField(verbose_name="设备", max_length=50)
    status = models.IntegerField(verbose_name="状态", default=0)
    arg_type = models.IntegerField(verbose_name="参数类型", default=0)
    arg = models.FloatField(verbose_name="参数值", default=0)

    def __str__(self):
        return {"id": self.device_id,
                "device_name": self.device_name,
                "status": self.status,
                "arg_type": self.arg_type,
                "arg": self.arg,
                "room_id": "",
                }

    class Meta:
        verbose_name = "设备"
        verbose_name_plural = verbose_name


class RoomDevice(models.Model):
    room_id = models.IntegerField(verbose_name="房间id")
    device_id = models.IntegerField(verbose_name="设备id")

    class Meta:
        verbose_name = "房间设备分配表"
        verbose_name_plural = verbose_name


class Scene(models.Model):
    scene_name = models.CharField(verbose_name="场景名称", max_length=20)
    status = models.IntegerField(verbose_name="状态", default=0)

    read_service_id = models.IntegerField(verbose_name='只读服务id', default=0)
    trigger_description = models.CharField(verbose_name='描述', max_length=256)
    trigger_condition = models.IntegerField(verbose_name='触发条件', default=0)
    trigger_value = models.FloatField(verbose_name='触发值', default=0.0)

    control_service_id = models.IntegerField(verbose_name='控制服务id', default=0)
    action_description = models.CharField('描述', max_length=256)
    action_value = models.BooleanField('动作值', default=False)

    def __str__(self):
        return {
            "id": self.id,
            "scene_name": self.scene_name,
            "status": self.status,
            'trigger': {
                'readserviceid': self.read_service_id,
                'condition': self.trigger_condition,
                'value': self.trigger_value
            },
            'action': {
                'controlserviceid': self.control_service_id,
                'value': self.action_value,
            }
        }

    class Meta:
        verbose_name = "场景"
        verbose_name_plural = verbose_name


class ReadService(models.Model):
    service_id = models.IntegerField(verbose_name='服务id', primary_key=True, default=0)
    name = models.CharField(verbose_name='name', max_length=100)
    aid = models.IntegerField(verbose_name="aid")
    iid = models.IntegerField(verbose_name="iid")
    allowed = models.IntegerField(verbose_name="允许值")
    description = models.CharField(verbose_name='描述', max_length=256)

    def __str__(self):
        return {
            "id": self.service_id, "aid": self.aid,
            "iid": self.iid, 'name':self.name,
            'allowed': self.allowed, 'description': self.description
        }

    class Meta:
        verbose_name = "只读服务"
        verbose_name_plural = verbose_name


class ControlService(models.Model):
    service_id = models.IntegerField(verbose_name='服务id', primary_key=True, default=0)
    name = models.CharField(verbose_name='name', max_length=100)
    aid = models.IntegerField(verbose_name="aid")
    iid = models.IntegerField(verbose_name="iid")
    allowed = models.IntegerField(verbose_name="允许值")
    description = models.CharField(verbose_name='描述', max_length=256)

    def __str__(self):
        return {
            "id": self.service_id, "aid": self.aid,
            "iid": self.iid, 'name':self.name,
            'allowed': self.allowed, 'description': self.description
        }

    class Meta:
        verbose_name = "控制服务"
        verbose_name_plural = verbose_name
