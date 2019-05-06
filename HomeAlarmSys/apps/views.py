from . import models
from .forms import UserForm, RegisterForm, EditForm
from django.shortcuts import render, redirect
import hashlib
from django.template import loader
from django.http import HttpResponse
from django.core import serializers
import json


def index(request):
    context = {}
    if not request.session.get("is_login", None):
        return redirect('/login/')
    else:
        return render(request, 'app/index.html')


def hash_code(s, salt='mysite'):  # 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def login(request):
    register_form = RegisterForm()
    if request.session.get('is_login', None):
        return redirect("/index/")

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(email=email)
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    request.session['email'] = user.email
                    request.session['phone'] = user.phone
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'app/login.html', locals())

    login_form = UserForm()
    return render(request, 'app/login.html', locals())


def register(request):
    login_form = UserForm()
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            phone = register_form.cleaned_data['phone']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'app/login.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'app/login.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'app/login.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = models.User.objects.create()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.phone = phone
                new_user.save()

                return redirect('/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'app/login.html', locals())


def user_manage(request):
    return render(request, 'app/user_manage.html', locals())


'''返回用户列表, 以json格式'''


def user_table(request):
    user_list = []

    all_user = models.User.objects.all()
    for user in all_user:
        user_list.append({'name': user.name, 'email': user.email, 'phone': user.phone})
    return HttpResponse(json.dumps(user_list), content_type='application/json; charset=utf-8')





def logout(request):
    request.session.flush()
    return redirect("/index/")


# 查看个人资料
def profile(request):
    if not request.session.get('is_login', None):
        return redirect("/index/")
    if request.method == "GET":
        username = request.session['user_name']
        phone = request.session['phone']
        email = request.session['email']
        return render(request, 'app/profile.html', locals())


def edit(request):
    if not request.session.get('is_login', None):
        return redirect("/index/")

    if request.method == "POST":
        edit_form = EditForm(request.POST)
        message = "请检查填写的内容！"
        payload = json.loads(request.body)
        username = payload.get('username')
        email = payload.get('email')
        phone = payload.get('phone')
        user = models.User.objects.get(id=request.session['user_id'])
        # print(username, email, phone, request.session['user_id'])
        user.name = username
        user.email = email
        user.phone = phone
        user.save()
        request.session['user_name'] = user.name
        request.session['email'] = user.email
        request.session['phone'] = user.phone
        return HttpResponse(200)
    return HttpResponse(500)
