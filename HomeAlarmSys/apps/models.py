from django.db import models
from django.contrib.auth.models import AbstractUser



class UserProfile(models.Model):
    role = models.PositiveSmallIntegerField(verbose_name="角色", choices=((1, '普通用户'), (2, '管理员'), (3, '超级管理员')), default=1)
    user_id = models.IntegerField(verbose_name="用户id")
    name = models.CharField(verbose_name="昵称", max_length=20)
    password =  models.CharField(verbose_name="密码", max_length=20)
    email = models.EmailField(verbose_name="邮箱")
    phone = models.CharField(verbose_name="手机", max_length=20)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['user_id']
        verbose_name = "用户"
        verbose_name_plural = verbose_name
    