# coding:utf-8
from datetime import datetime

from django.db import models
from users.models import UserProfile
from courses.models import Course
from organization.models import CourseOrg


# Create your models here.

class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name="用户姓名")
    mobile = models.CharField(max_length=11, verbose_name="手机号码")
    course_name = models.CharField(max_length=50, verbose_name="课程名称")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户咨询"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}"


class CourseComments(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    comments = models.CharField(max_length=250, verbose_name="评论")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="评论时间")

    class Meta:
        verbose_name = "课程评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.comments}"


class UserFavorite(models.Model):
    TYPE_CHOICES = ((1, "课程"), (2, "课程机构"), (3, "讲师"))

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    fav_id = models.IntegerField(default=0, verbose_name="不同类型数据的ID")
    fav_type = models.CharField(choices=TYPE_CHOICES, default=1, verbose_name="收藏类型", max_length=50)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="收藏时间")

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.fav_id}"


class UserMessage(models.Model):
    user = models.IntegerField(default=0, verbose_name="接收消息的用户")
    message = models.CharField(max_length=500, verbose_name="消息内容")
    has_read = models.BooleanField(default=False, verbose_name="是否已读")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = "用户消息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.message}"


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户学习的课程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.course}"
