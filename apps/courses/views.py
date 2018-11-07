from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.db.models import Q

from .models import Course, CourseResource,Video
from operation.models import UserFavorite, CourseComments, UserCourse

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from utils.mixin_utils import LoginRequiredMixin


class CourseListView(View):
    @staticmethod
    def get(request):
        all_courses = Course.objects.all().order_by("-add_time")
        # 热门
        hot_courses = Course.objects.all().order_by("-click_nums")[:3]
        # 搜索
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) | Q(detail__icontains=search_keywords))
        # 排序
        sort = request.GET.get("sort", "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")

        # 对课程进行分页
        try:
            page = request.GET  .get("page", 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 6, request=request)
        courses = p.page(page)

        return render(request, "course-list.html", {
            "all_course": courses,
            "sort": sort,
            "hot_courses": hot_courses,
            # "search_keywords": search_keywords
        })


class CourseDetailView(View):
    @staticmethod
    def get(request, course_id):
        courses = Course.objects.get(id=int(course_id))
        courses.click_nums += 1
        courses.save()

        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=courses.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=courses.course_org.id, fav_type=2):
                has_fav_org = True

        tag = courses.tag
        if tag:
            related_course = Course.objects.filter(tag=tag)[1:2]
        else:
            related_course = []

        return render(request, "course-detail.html", {
            "course": courses,
            "relate_courses": related_course,
            "has_fav_course": has_fav_course,
            "has_fav_org": has_fav_org,
        })


class CourseInfoView(LoginRequiredMixin, View):
    @staticmethod
    def get(request, course_id):
        course = Course.objects.get(id=int(course_id))
        user_courses = UserCourse.objects.filter(course=course).filter(user=request.user)
        if not user_courses:
            UserCourse.objects.create(user=request.user, course=course)
        user_ids = [i.get("user") for i in UserCourse.objects.filter(course=course).values("user")]
        all_user_courses = [i.get("course") for i in UserCourse.objects.filter(user_id__in=user_ids).values("course")]
        all_user_courses = list(set(all_user_courses))
        all_user_courses.remove(int(course_id))
        relate_courses = Course.objects.filter(id__in=all_user_courses).order_by("-click_nums")[:5]
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, "course-video.html", {
            "course": course,
            "all_resources": all_resources,
            "relate_courses": relate_courses,
        })


class CommentsView(LoginRequiredMixin, View):
    @staticmethod
    def get(request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.filter(course=course).order_by("-pk")
        return render(request, "course-comment.html", {
            "course": course,
            "all_resources": all_resources,
            "all_comments": all_comments,
        })


class AddCommentsView(View):
    @staticmethod
    def post(request):
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"error","msg":"用户未登录"}', content_type='application/json')
        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")
        if int(course_id) > 0 and comments:
            CourseComments.objects.create(course=Course.objects.get(id=int(course_id)),
                                          comments=comments,
                                          user=request.user
                                          )
            return HttpResponse('{"status":"success","msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"error","msg":"添加失败"}', content_type='application/json')


class VideoPlayView(View):
    @staticmethod
    def get(request,video_id):
        video = Video.objects.filter(id=int(video_id)).first()
        course = video.lesson.course
        course.students += 1
        course.save()

        # course = Course.objects.get(id=int(course_id))
        user_courses = UserCourse.objects.filter(course=course).filter(user=request.user)
        if not user_courses:
            UserCourse.objects.create(user=request.user,course=course)
        user_ids = [i.get("user") for i in UserCourse.objects.filter(course=course).values("user")]
        all_user_courses = [i.get("course") for i in UserCourse.objects.filter(user_id__in=user_ids).values("course")]
        all_user_courses = list(set(all_user_courses))
        all_user_courses.remove(int(course.pk))
        relate_courses = Course.objects.filter(id__in=all_user_courses).order_by("-click_nums")[:5]
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, "course-play.html", {
            "course": course,
            "all_resources": all_resources,
            "relate_courses": relate_courses,
            "video":video
        })
