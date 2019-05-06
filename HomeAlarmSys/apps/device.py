from . import models
from .forms import UserForm, RegisterForm, EditForm
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
        device_list.append(json.loads(device.__str__()))
    return HttpResponse(json.dumps(device_list), content_type='application/json; charset=utf-8')


def device_add(request):

    data = json.loads(request.body)
    device = models.Device.objects.create(device_id = data.get('id'),
                                          device_name=data.get("device_name"),
                                          status=data.get('status')
                                        )
    return HttpResponse(200)


def device_get(request):
    device_id = json.loads(request.body).get("deviceId")
    device = models.Device.objects.get(device_id=device_id)
    return HttpResponse(device, content_type="application/json; charset=utf-8")


def device_update(request):
    data = json.loads(request.body)
    device_id = data.get('id')
    device_name = data.get('device_name')
    status = data.get('status')
    device = models.Device.objects.get(id=device_id)
    device.status = status
    device.device_name = device_name
    device.save()
    return HttpResponse(200)


def device_delete(request):
    ids = json.loads(request.body).get("idString")
    id_list = ids.split(",")
    for i in id_list:
        models.Device.objects.get(device_id=i).delete()
    return HttpResponse(200)
