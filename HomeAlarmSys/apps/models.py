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
        return self.room_name

    class Meta:
        verbose_name = "房间"
        verbose_name_plural = verbose_name


class Device(models.Model):
    type = models.CharField(verbose_name="设备", max_length=20)
    enable = models.CharField(verbose_name="能否使用", max_length=20)

    class Meta:
        verbose_name = "设备"
        verbose_name_plural = verbose_name


class DeviceArg(models.Model):
    device_id = models.CharField(verbose_name="设备id", max_length=20)
    arg_name = models.CharField(verbose_name="参数名称", max_length=20)
    value = models.IntegerField(verbose_name="参数值")

    def __str__(self):
        return self.arg_name

    class Meta:
        verbose_name = "设备参数"
        verbose_name_plural = verbose_name


class Scene(models.Model):
    scene_name = models.CharField(verbose_name="场景名称", max_length=20)
    status = models.IntegerField(verbose_name="状态", default=0)

    def __str__(self):
        return json.dumps({"id": self.id, "scene_name": self.scene_name, 'status': self.status})

    class Meta:
        verbose_name = "场景"
        verbose_name_plural = verbose_name
