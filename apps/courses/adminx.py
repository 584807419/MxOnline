from .models import Course, Lesson, Video, CourseResource, BannerCourse

import xadmin


class LessinInLine(object):
    model = Lesson
    extra = 0


class CourseResourceInline(object):
    model = CourseResource
    extra = 0


class CourseAdmin(object):
    list_display = ["name", "desc", "detail", "degree", "learn_times", "students", "fav_nums", "image", "click_nums",
                    "add_time", 'get_zj_nums', 'go_to']
    search_fields = ["name", "desc", "detail", "degree", "learn_times", "students", "fav_nums", "image", "click_nums",
                     "add_time"]
    list_filter = ["name", "desc", "detail", "degree", "learn_times", "students", "fav_nums", "image", "click_nums",
                   "add_time"]
    ordering = ['-click_nums']  # 排序
    readonly_fields = ['click_nums']  # 设置只读无法后台修改了就
    exclude = ['fav_nums']  # 不显示，和readonly_fields冲突
    model_icon = "fa fa-cog fa-spin fa-la fa-fw"
    inlines = [LessinInLine, CourseResourceInline]  # 课程编辑后台添加章节信息,嵌套只能做一层
    list_editable = ['degree', 'desc']
    refresh_times = [3, 5]  # 定时刷新页面显示数据
    style_fields = {"detail": "ueditor"} # 指定detail字段的样式是ueditor,然后插件中对ueditor这个样式进行识别

    def save_models(self):  # 重载save_models 方法,新增和修改都会走这个接口
        # 在保存课程的时候统计课程机构の课程数
        obj = self.new_obj
        obj.save()
        if obj.course_org:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()


xadmin.site.register(Course, CourseAdmin)


class BannerCourseAdmin(object):  # 同一model注册两个管理器
    list_display = ["name", "desc", "detail", "degree", "learn_times", "students", "fav_nums", "image", "click_nums",
                    "add_time"]
    search_fields = ["name", "desc", "detail", "degree", "learn_times", "students", "fav_nums", "image", "click_nums",
                     "add_time"]
    list_filter = ["name", "desc", "detail", "degree", "learn_times", "students", "fav_nums", "image", "click_nums",
                   "add_time"]
    ordering = ['-click_nums']  # 排序
    readonly_fields = ['click_nums']  # 设置只读无法后台修改了就
    exclude = ['fav_nums']  # 不显示，和readonly_fields冲突
    model_icon = "fa fa-cog fa-spin fa-la fa-fw"
    inlines = [LessinInLine, CourseResourceInline]  # 课程编辑后台添加章节信息,嵌套只能做一层

    def queryset(self):  # 重载queryset方法达到过滤目的
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


xadmin.site.register(BannerCourse, BannerCourseAdmin)


class LessonAdmin(object):
    list_display = ["course", "name", "add_time"]
    search_fields = ["course", "name"]
    list_filter = ["course__name", "name", "add_time"]  # 两个下划线表示外键的某个字段来过滤
    model_icon = "fa fa-cog fa-spin fa-la fa-fw"


xadmin.site.register(Lesson, LessonAdmin)


class VideoAdmin(object):
    list_display = ["lesson", "name", "add_time"]
    search_fields = ["lesson", "name"]
    list_filter = ["lesson", "name", "add_time"]
    model_icon = "fa fa-cog fa-spin fa-la fa-fw"


xadmin.site.register(Video, VideoAdmin)


class CourseResourceAdmin(object):
    list_display = ["course", "name", "download", "add_time"]
    search_fields = ["course", "name", "download"]
    list_filter = ["course", "name", "download", "add_time"]
    model_icon = "fa fa-cog fa-spin fa-la fa-fw"


xadmin.site.register(CourseResource, CourseResourceAdmin)
