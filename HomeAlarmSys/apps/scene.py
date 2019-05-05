from . import models
from .forms import UserForm, RegisterForm, EditForm
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
        scene_list.append({"id": scene.id, "scene_name": scene.scene_name, "status": scene.status})
    return HttpResponse(json.dumps(scene_list), content_type='application/json; charset=utf-8')


def scene_add(request):
    scene = models.Scene.objects.create()

    scene.scene_name = json.loads(request.body).get('scene_name')
    scene.status = json.loads(request.body).get('status')
    scene.save()
    return HttpResponse(200)


def scene_get(request):
    scene_id = json.loads(request.body).get("sceneId")
    scene = models.Scene.objects.get(id=scene_id)
    return HttpResponse(scene, content_type="application/json; charset=utf-8")


def scene_update(request):
    data = json.loads(request.body)
    scene_id = data.get('id')
    scene_name = data.get('scene_name')
    status = data.get('status')
    scene = models.Scene.objects.get(id=scene_id)
    scene.status = status
    scene.scene_name = scene_name
    scene.save()
    return HttpResponse(200)


def scene_delete(request):
    ids = json.loads(request.body).get("idString")
    id_list = ids.split(",")
    for i in id_list:
        models.Scene.objects.get(id=i).delete()
    return HttpResponse(200)
