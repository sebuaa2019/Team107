from .. import models
from ..forms import UserForm, RegisterForm, EditForm
from django.shortcuts import render, redirect
import hashlib
from django.template import loader
from django.http import HttpResponse
from django.core import serializers
import json


def device_manage(request):
    return render(request, 'app/device_manage.html')


def device_table(request):
    device_list = []
    all_device = models.Device.objects.all()
    for device in all_device:
        temp = device.__str__()
        device_id = temp.get('id')
        device_map = models.RoomDevice.objects.filter(device_id=device_id)
        if len(device_map) != 0:
            temp['room_id'] = device_map[0].room_id
        device_list.append(temp)
    return HttpResponse(json.dumps(device_list), content_type='application/json; charset=utf-8')


def device_add(request):
    data = json.loads(request.body)
    device = models.Device.objects.create(device_id=data.get('id'),
                                          device_name=data.get("device_name"),
                                          status=data.get('status')
                                          )
    return HttpResponse(200)


def device_get(request):
    device_id = json.loads(request.body).get("deviceId")
    device = models.Device.objects.get(device_id=device_id).__str__()
    device_map = models.RoomDevice.objects.filter(device_id=device_id)
    if len(device_map) != 0:
        device['room_id'] = device_map[0].room_id
    return HttpResponse(json.dumps(device), content_type="application/json; charset=utf-8")


def device_update(request):
    data = json.loads(request.body)
    device_id = data.get('id')
    device_name = data.get('device_name')
    status = data.get('status')
    room_id = data.get('room')

    device_map = models.RoomDevice.objects.filter(device_id=device_id)
    if len(device_map) == 0:
        room_device = models.RoomDevice.objects.create(device_id=device_id, room_id=room_id)

    else:
        room_device = device_map[0]
        room_device.room_id = room_id
    room_device.save()

    device = models.Device.objects.get(device_id=device_id)
    device.status = status
    device.device_name = device_name
    device.save()
    return HttpResponse(200)


def device_upload(request):
    device_info = json.loads(request.body)
    sensors = device_info.get('sensors')
    accessories = device_info.get('accessories')

    for sensor in sensors:
        sensor_id = sensor.get('aid')
        arg_info = sensor.get('type')
        arg_type = arg_info.get('valuetype')  # 参数类型: 0连续型, 1布尔型
        arg = arg_info.get('currentvalue')  # 参数值
        device = models.Device.objects.filter(device_id=sensor_id)
        if len(device) == 0:
            device = models.Device.objects.create(device_id=sensor_id,
                                                  arg_type=arg_type,
                                                  arg=arg)
        else:
            device = device[0]
            device.arg_type = arg_type
            device.arg = arg
        device.status = 1
        device.save()

    return HttpResponse(200)


def device_delete(request):
    ids = json.loads(request.body).get("idString")
    id_list = ids.split(",")
    for i in id_list:
        models.Device.objects.get(device_id=i).delete()
    return HttpResponse(200)


def device_alarm(request):
    pass


def device_fire(request):
    pass


def device_smoke(request):
    pass
