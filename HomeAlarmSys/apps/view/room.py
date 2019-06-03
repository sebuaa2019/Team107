from .. import models
from ..forms import UserForm, RegisterForm, EditForm
from django.shortcuts import render, redirect
import hashlib
from django.template import loader
from django.http import HttpResponse
from django.core import serializers
import json


def room_add(request):
    room = models.Room.objects.create()
    room.room_name = json.loads(request.body).get('room_name')
    room.save()
    return HttpResponse("200")


def room_manage(request):
    return render(request, 'app/room_manage.html', locals())


def room_table(request):
    room_list = []
    all_room = models.Room.objects.all()
    for room in all_room:
        room_list.append({"id": room.id, "room_name": room.room_name})
    return HttpResponse(json.dumps(room_list), content_type='application/json; charset=utf-8')


def room_get(request):
    room_id = json.loads(request.body).get("roomId")
    room = models.Room.objects.get(id=room_id)
    return HttpResponse(json.dumps(room.__str__()), content_type="application/json; charset=utf-8")
    #return HttpResponse(room, content_type="application/json; charset=utf-8")


def room_update(request):
    data = json.loads(request.body)
    room_id = data.get('id')
    room_name = data.get('room_name')
    room = models.Room.objects.get(id=room_id)
    room.room_name = room_name
    room.save()
    return HttpResponse(200)


def room_delete(request):
    ids = json.loads(request.body).get("idString")
    id_list = ids.split(",")
    for i in id_list:
        models.Room.objects.get(id=i).delete()
    return HttpResponse(200)


def room_list(request):
    rooms = models.Room.objects.all()
    room_l = []
    for r in rooms:
        room_l.append(r.__str__())
    return HttpResponse(json.dumps(room_l), content_type='application/json; charset=utf-8')
