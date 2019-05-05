from django import forms
from captcha.fields import CaptchaField


class UserForm(forms.Form):
    email = forms.CharField(label="邮箱", max_length=128, widget=forms.TextInput(attrs={
        'class': 'form-control', 'type': 'email', 'placeholder': '邮箱地址'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'type': 'password', 'placeholder': '密码'}))
    # captcha = CaptchaField(label='验证码')


###
class RegisterForm(forms.Form):  # type="text" class="form-control" placeholder="Username"
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={
        'class': 'form-control', 'type': 'text', 'placeholder': '用户名'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'type': 'password', 'placeholder': '密码'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'type': 'password', 'placeholder': '确认密码'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={
        'class': 'form-control', 'type': 'email', 'placeholder': '邮箱地址'}))
    phone = forms.CharField(label="联系电话", max_length=20, widget=forms.TextInput(attrs={
        'class': 'form-control', 'type': 'text', 'placeholder': '联系电话'}))
    # captcha = CaptchaField(label='验证码')


class EditForm(forms.Form):
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label="联系电话", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # extra_form = forms.CharField(label='info', max_length=255)
    # captcha = CaptchaField(label='验证码')



