from .. import models
from ..forms import UserForm, RegisterForm, EditForm
from django.shortcuts import render, redirect
import hashlib
from django.template import loader
from django.http import HttpResponse
from django.core import serializers
import json


def scene_manage(request):
    return render(request, 'app/scene_manage.html')


def scene_table(request):
    scene_list = []
    all_scene = models.Scene.objects.all()
    for scene in all_scene:
        scene_list.append(scene.__str__())
    return HttpResponse(json.dumps(scene_list), content_type='application/json; charset=utf-8')


def scene_add(request):
    scene = models.Scene.objects.create()
    info = json.loads(request.body)
    scene.scene_name = info.get('scene_name')
    scene.read_service_id = info.get('tri-service')
    scene.control_service_id = info.get('action-service')
    scene.trigger_value = info.get('arg')
    scene.action_value = info.get('of-value')
    scene.status = info.get('status')
    scene.save()
    return HttpResponse(200)


def scene_get(request):
    scene_id = json.loads(request.body).get("sceneId")
    scene = models.Scene.objects.get(id=scene_id)
    return HttpResponse(json.dumps(scene.__str__()), content_type="application/json; charset=utf-8")


def scene_update(request):
    info = json.loads(request.body)
    scene_id = info.get('id')
    scene = models.Scene.objects.get(id=scene_id)
    scene.scene_name = info.get('scene_name')
    scene.read_service_id = info.get('tri-service')
    scene.control_service_id = info.get('action-service')
    scene.trigger_value = info.get('arg')
    scene.action_value = info.get('of-value')
    scene.status = info.get('status')
    scene.save()
    return HttpResponse(200)


def scene_delete(request):
    ids = json.loads(request.body).get("idString")
    id_list = ids.split(",")
    for i in id_list:
        models.Scene.objects.get(id=i).delete()
    return HttpResponse(200)


'''
更新数据库中服务信息, 有就更新, 无就新建
'''


def db_service_update(service_id, aid, iid, allowed, description, name, _type):
    if _type == 0:
        service = models.ReadService.objects.filter(service_id=service_id)
    else:
        service = models.ControlService.objects.filter(service_id=service_id)

    if len(service) == 0:
        if _type == 0:
            service = models.ReadService.objects.create(
                service_id=service_id, name=name,
                aid=aid, iid=iid, allowed=allowed,
                description=description)
        else:
            service = models.ControlService.objects.create(
                service_id=service_id, name=name,
                aid=aid, iid=iid, allowed=allowed,
                description=description)
    else:
        service = service[0]
        service.aid = aid
        service.iid = iid
        service.name = name
        service.allowed = allowed
        service.description = description
    service.save()
    return


def scene_service(request):
    read_service = json.loads(request.body).get('readservices')
    control_service = json.loads(request.body).get('controlservices')

    _type = 0
    for ser in read_service:
        service_id = ser.get('id')
        aid = ser.get('aid')
        iid = ser.get('iid')
        allowed = ser.get('allowed_condition')
        description = ser.get('description')
        name = ser.get('name')
        db_service_update(service_id, aid, iid,
                          allowed, description, name, _type)

    _type = 1
    for ser in control_service:
        service_id = ser.get('id')
        aid = ser.get('aid')
        iid = ser.get('iid')
        allowed = ser.get('allowed_value')
        description = ser.get('description')
        name = ser.get('name')
        db_service_update(service_id, aid, iid, allowed, description, name, _type)

    # 返回场景信息
    scene_list = []
    for sc in models.Scene.objects.all():
        scene_list.append(sc.__str__())

    return HttpResponse(json.dumps({'scenes':scene_list}),
                        content_type='application/json; charset=utf-8')


def service_list(request):
    readService = []
    controlService = []

    for service in models.ReadService.objects.all():
        readService.append(service.__str__())
    for service in models.ControlService.objects.all():
        controlService.append(service.__str__())

    return HttpResponse(
        json.dumps({'readService': readService,
                    'controlService': controlService}),
        content_type="application/json; charset=utf-8"
    )
