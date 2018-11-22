from .models import Course, Lesson, Video, CourseResource

import xadmin


class CourseAdmin(object):
    list_display = ["name", "desc", "detail", "degree", "learn_times", "students", "fav_nums", "image", "click_nums",
                    "add_time"]
    search_fields = ["name", "desc", "detail", "degree", "learn_times", "students", "fav_nums", "image", "click_nums",
                     "add_time"]
    list_filter = ["name", "desc", "detail", "degree", "learn_times", "students", "fav_nums", "image", "click_nums",
                   "add_time"]
    ordering = ['-click_nums'] # 排序
    readonly_fields = ['click_nums'] # 设置只读无法后台修改了就
    exclude = ['fav_nums'] # 不显示，和readonly_fields冲突


xadmin.site.register(Course, CourseAdmin)


class LessonAdmin(object):
    list_display = ["course", "name", "add_time"]
    search_fields = ["course", "name"]
    list_filter = ["course__name", "name", "add_time"]  # 两个下划线表示外键的某个字段来过滤


xadmin.site.register(Lesson, LessonAdmin)


class VideoAdmin(object):
    list_display = ["lesson", "name", "add_time"]
    search_fields = ["lesson", "name"]
    list_filter = ["lesson", "name", "add_time"]


xadmin.site.register(Video, VideoAdmin)


class CourseResourceAdmin(object):
    list_display = ["course", "name", "download", "add_time"]
    search_fields = ["course", "name", "download"]
    list_filter = ["course", "name", "download", "add_time"]


xadmin.site.register(CourseResource, CourseResourceAdmin)
