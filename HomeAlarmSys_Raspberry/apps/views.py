from django.shortcuts import render
from django.shortcuts import redirect
import hashlib
from django.template import loader
from django.http import HttpResponse
from django.core import serializers
import json
from . import models
from django import forms
from django.http import JsonResponse

def index(request):
    return HttpResponse("hello\r\n")

def switch_on(request):
    obj = models.Switch.objects.first()
    if(obj == None):
        obj = models.Switch.objects.create()
    obj.switch = True
    obj.save()
    return HttpResponse("success")

def switch_off(request):
    obj = models.Switch.objects.first()
    if(obj == None):
        obj = models.Switch.objects.create()
    obj.switch = False
    obj.save()
    return HttpResponse("success")

def sensor_db(request):
    obj = models.Info.objects.first()
    return JsonResponse({"temperature":obj.temperature,"humidity":obj.humidity,"occupancy":obj.occupancy,"smoke":obj.smoke})

def sensor(request):
    if request.method == 'POST':
        content = json.loads(request.body.decode())
    return HttpResponse("26.5")

def accessory(request):
    return HttpResponse("accessory response\r\n")

def alarm(request):
    if request.method == 'POST':
        print(request.POST)
        print(request.body)
        print(request.body.decode())
    return HttpResponse("success")
