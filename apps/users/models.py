from datetime import datetime

from django.db import models

from django.contrib.auth.models import AbstractUser
from utils.db_tools import MxModelUpdate


class UserProfile(AbstractUser, MxModelUpdate):
    nick_name = models.CharField(max_length=50, default="", verbose_name="昵称")
    birthday = models.DateField(null=True, blank=True, verbose_name="生日")
    gender = models.CharField(choices=(("male", "男"), ("female", "女")), max_length=6, default="female",
                              verbose_name="性别")
    address = models.CharField(max_length=100, default="", null=True, blank=True, verbose_name="地址")
    mobile = models.CharField(max_length=11, verbose_name="电话", null=True, blank=True, default="")
    image = models.ImageField(max_length=100, upload_to="image/%Y/%m", default="image/default.jpg", null=True,
                              blank=True, verbose_name="用户头像")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model, MxModelUpdate):
    code = models.CharField(max_length=40, verbose_name="验证码")
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    send_type = models.CharField(choices=(("register", "注册"), ("forget", "找回密码"), ("update_email", "修改邮箱")), max_length=30)
    send_time = models.DateTimeField(default=datetime.now, verbose_name="发送时间")  # now不加括号(),否则刚开始编译就执行了

    class Meta:
        verbose_name = "邮箱验证码 "
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.email}__{self.code}'


class Banner(models.Model, MxModelUpdate):
    title = models.CharField(max_length=100, verbose_name="标题")
    image = models.ImageField(upload_to="banner/%Y/%m", verbose_name="轮播图")
    url = models.URLField(max_length=200, verbose_name="访问地址")
    index = models.IntegerField(default=100, verbose_name="顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name
