from .. import models
from ..forms import UserForm, RegisterForm, EditForm
from django.shortcuts import render, redirect
import hashlib
from django.template import loader
from django.http import HttpResponse
from django.core import serializers
import json
import requests
import time

URL = 'https://sc.ftqq.com/SCU51140T3ac7e7e2b2032b1a7bf562f03d19d5405cd66313d0f96.send'


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


def db_device_update(device_id, arg_type, arg, device_type, device_name=" "):
    device = models.Device.objects.filter(device_id=device_id)
    if len(device) == 0:
        device = models.Device.objects.create(device_id=device_id,
                                              arg_type=arg_type,
                                              arg=arg,
                                              device_name=device_name,
                                              device_type=device_type)
    else:
        device = device[0]
        device.arg_type = arg_type
        device.arg = arg
        device.device_type = device_type
    device.status = 1
    device.save()
    return


def alarm_detect():
    localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    data = {
        'text': 'AAA家庭报警装置提醒',
        'desp': '家中疑似发现入侵行为！' + " message id: " + localtime,
    }
    alarm_control = models.Device.objects.get(device_id="70010")
    body_sensor = models.Device.objects.get(device_id="50025")
    if alarm_control.arg == 1 and body_sensor.arg == 1:
        # print("alarm！")
        r = requests.post(URL, data=data)
        # print(r.text)


def fire_detect():
    localtime = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    # print(localtime)
    data = {
        'text': 'AAA家庭报警装置提醒',
        'desp': '家中疑似发生火灾！' + "message id: " + localtime,
    }
    alarm_control = models.Device.objects.get(device_id="70010")
    fire_sensor = models.Device.objects.get(device_id="50019")
    if alarm_control.arg == 1 and fire_sensor.arg == 1:
        # print("alarm！fire")
        r = requests.post(URL, data=data)
        # print(r.text)


def device_upload(request):
    device_info = json.loads(request.body)
    sensors = device_info.get('sensors')
    accessories = device_info.get('accessories')

    for sensor in sensors:
        sensor_id = int(sensor.get('aid')) * 10000 + int(sensor.get('iid'))
        arg_info = sensor.get('type')
        device_name = sensor.get('name')
        arg_type = arg_info.get('valuetype')  # 参数类型: 0连续型, 1布尔型
        arg = arg_info.get('currentvalue')  # 参数值
        db_device_update(sensor_id, arg_type, arg, 0, device_name)

    for acc in accessories:
        aid = acc.get('aid')
        idds = acc.get('iids')
        device_name = acc.get('name')
        for item in idds:
            iid = item.get('iid')
            device_id = int(aid) * 10000 + int(iid)
            arg_type = item.get('valuetype')
            arg = item.get('currentvalue')
            db_device_update(device_id, arg_type, arg, 1, device_name)

    alarm_detect()
    fire_detect()

    acc_list = []
    aid_list = []
    acc_devs = models.Device.objects.filter(device_type=1)
    for ac in acc_devs:
        aid_list.append(ac.device_id // 10000)

    aid_list = set(aid_list)
    for aid in aid_list:
        ac_dict = {'aid': aid, 'name': '', 'iids': []}
        for ac in acc_devs:
            if aid == ac.device_id // 10000:
                ac_dict['name'] = ac.device_name
                iid = {'iid': ac.device_id % 10000, 'valuetype': ac.arg_type, 'currentvalue': ac.arg}
                if ac.arg_type == 1:
                    if iid['currentvalue'] == 0:
                        iid['currentvalue'] = False
                    else:
                        iid['currentvalue'] = True
                ac_dict['iids'].append(iid)
        acc_list.append(ac_dict)
    # print(acc_list)
    return HttpResponse(json.dumps({"accessories": acc_list}),
                        content_type='application/json; charset=utf-8')


def device_delete(request):
    ids = json.loads(request.body).get("idString")
    id_list = ids.split(",")
    for i in id_list:
        models.Device.objects.get(device_id=i).delete()
    return HttpResponse(200)


def device_alarm(request):
    info = {'alarm_control': 0, 'alarm_info': 0}
    alarm_control = models.Device.objects.get(device_id="70010")
    body_sensor = models.Device.objects.get(device_id="50025")

    info['alarm_control'] = alarm_control.arg
    info['alarm_info'] = body_sensor.arg

    return HttpResponse(json.dumps(info), content_type='application/json; charset=utf-8')


def device_fire(request):
    info = {'alarm_control': 0, 'fire_info': 0}
    alarm_control = models.Device.objects.get(device_id="70010")
    fire_sensor = models.Device.objects.get(device_id="50019")

    info['alarm_control'] = alarm_control.arg
    info['fire_info'] = fire_sensor.arg

    return HttpResponse(json.dumps(info), content_type='application/json; charset=utf-8')


def device_smoke(request):
    pass


def device_on_off(request):
    device_id = request.GET.get('id')
    device = models.Device.objects.filter(device_id=device_id)[0]
    if device.arg == 1:
        device.arg = 0
    else:
        device.arg = 1
    device.save()
    return HttpResponse(200)


def control_device_list(request):
    device_list = []
    ret = models.Device.objects.filter(device_type=1, arg_type=1)
    for de in ret:
        device_list.append(de.__str__())
    return HttpResponse(json.dumps(device_list), content_type="application/json; charset=utf-8")
