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
from ..config import *


def local_error(request):
    localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    data = {
        'text': 'AAA设备提醒',
        'desp': '家中部分设备出现故障!' #+ " message id: " + localtime,
    }
    r = requests.post(URL, data=data)
    return HttpResponse(200)
