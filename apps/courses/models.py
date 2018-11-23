from datetime import datetime

from django.db import models

from organization.models import CourseOrg, Teacher


# Create your models here.

class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name="课程机构", null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name="课程名称")
    desc = models.CharField(max_length=300, verbose_name="课程描述")
    detail = models.TextField(verbose_name="课程详情")
    teacher = models.ForeignKey(Teacher, verbose_name="讲师", null=True, blank=True, on_delete=models.CASCADE)
    degree = models.CharField(choices=(("1", "初级"), ("2", "中级"), ("3", "高级")), verbose_name="课程等级", default="1",
                              max_length=50)
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟)")
    students = models.IntegerField(default=0, verbose_name="学生人数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏人数")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name="封面图", null=True, blank=True)
    click_nums = models.IntegerField(default=0, verbose_name="点击量")
    category = models.CharField(max_length=20, verbose_name="课程类别", default="后端开发")
    tag = models.CharField(max_length=15, verbose_name="课程标签", default="", null=True, blank=True)
    youneed_know = models.CharField(default="", max_length=300, verbose_name="课程须知", null=True, blank=True)
    teacher_tell = models.CharField(default="", max_length=300, verbose_name="老师告诉你", null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    is_banner = models.BooleanField(default=False, verbose_name="是否轮播图")

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        return self.lesson_set.all().count()
    get_zj_nums.short_description = "章节数"

    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href='http://www.devnav.win'>跳转</>")

    def get_course_lesson(self):
        return self.lesson_set.all()

    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    def __str__(self):
        return f"{self.name}"


class BannerCourse(Course): # 同一model注册两个管理器
    class Meta:
        verbose_name = "轮播课程"
        verbose_name_plural = verbose_name
        proxy = True


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name="课程", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="章节名称")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name

    def get_lesson_video(self):
        """获取章节视频"""
        return self.video_set.all()

    def __str__(self):
        return f"{self.name}"


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name="章节", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="视频名称")
    url = models.CharField(max_length=255, default="http://www.devnav.win/", verbose_name="访问地址")
    learn_times = models.IntegerField(default=0, verbose_name="视频时长(分钟)")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}"


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name="课程", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="下载资源名称")
    download = models.FileField(upload_to="course/resource/%Y/%m", verbose_name="资源文件", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程下载资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name}"
