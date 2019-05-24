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


def service_table(request):
    service_list = []
    all_service = models.ControlService.objects.all()
    for ser in all_service:
        service_list.append(ser.__str__())

    all_service = models.ReadService.objects.all()
    for ser in all_service:
        service_list.append(ser.__str__())
    return HttpResponse(json.dumps(service_list), content_type='application/json; charset=utf-8')
