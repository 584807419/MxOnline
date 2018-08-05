from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, default="", verbose_name="昵称")
    birthday = models.CharField(null=True, blank=True, verbose_name="生日")
    gender = models.CharField(choices=(("male", "男"), ("female", "女")), default="female", verbose_name="性别")
    address = models.CharField(max_length=100, default="", null=True, blank=True, verbose_name="地址")
    mobile = models.CharField(max_length=11, verbose_name="电话", null=True, blank=True, default="")
    image = models.ImageField(max_length=100, upload_to="image/%Y/%m", default="image/default.jpg", null=True,
                              blank=True, verbose_name="用户头像")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
