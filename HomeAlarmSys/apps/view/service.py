from .. import models
from ..forms import UserForm, RegisterForm, EditForm
from django.shortcuts import render, redirect
import hashlib
from django.template import loader
from django.http import HttpResponse
from django.core import serializers
import json


def service_manage(request):
    return render(request, 'app/service_manage.html')


def service_table_tri(request):
    service_list = []
    all_service = models.ReadService.objects.all()
    for ser in all_service:
        service_list.append(ser.__str__())
    return HttpResponse(json.dumps(service_list), content_type='application/json; charset=utf-8')


def service_table_act(request):
    service_list = []
    all_service = models.ControlService.objects.all()
    for ser in all_service:
        service_list.append(ser.__str__())
    return HttpResponse(json.dumps(service_list), content_type='application/json; charset=utf-8')


def service_delete_tri(request):
    ids = json.loads(request.body).get("idString")
    id_list = ids.split(",")
    for i in id_list:
        models.ReadService.objects.get(service_id=i).delete()
    return HttpResponse(200)


def service_delete_act(request):
    ids = json.loads(request.body).get("idString")
    id_list = ids.split(",")
    for i in id_list:
        models.ControlService.objects.get(service_id=i).delete()
    return HttpResponse(200)
