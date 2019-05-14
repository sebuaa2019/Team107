from django.db import models
import json

class Room(models.Model):
    room_name = models.CharField(verbose_name="房间名称", max_length=20)
    def __str__(self):
        return {"id": self.id, "room_name": self.room_name}
    class Meta:
        verbose_name = "房间"
        verbose_name_plural = verbose_name

class Device(models.Model):
    device_id = models.IntegerField(verbose_name="设备id", primary_key=True)
    device_name = models.CharField(verbose_name="设备", max_length=20)
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
    def __str__(self):
        return json.dumps({"id": self.id, "scene_name": self.scene_name, 'status': self.status})
    class Meta:
        verbose_name = "场景"
        verbose_name_plural = verbose_name

class Switch(models.Model):
    switch = models.BooleanField(default=False,verbose_name="开关")
    class Meta:
        verbose_name = "开关表"
        verbose_name_plural = verbose_name
class Info(models.Model):
    temperature = models.FloatField(verbose_name="温度")
    humidity = models.FloatField(verbose_name="湿度")
    occupancy = models.BooleanField(verbose_name="人体")
    smoke = models.BooleanField(verbose_name="烟")
    class Meta:
        verbose_name = "开关表"
        verbose_name_plural = verbose_name

