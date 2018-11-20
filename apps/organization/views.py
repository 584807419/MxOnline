from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.db.models import Q

from .models import CourseOrg, CityDict, Teacher
from operation.models import UserFavorite
from courses.models import Course
from .forms import UserAskForm

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.


class OrgView(View):
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        all_citys = CityDict.objects.all()
        # 热门机构
        hot_orgs = all_orgs.order_by("-click_nums")[:3]

        # 搜索
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))

        # 取出筛选的城市
        city_id = request.GET.get("city") if request.GET.get("city") else ""
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))
        # 类别筛选
        category = request.GET.get("ct", "")
        if category:
            all_orgs = all_orgs.filter(category=category)
        # 人数和课程数排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")

        org_nums = all_orgs.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        page = str(page)
        p = Paginator(all_orgs, 5, request=request)
        orgs = p.page(page)
        return render(request, "org-list.html",
                      {"all_orgs": orgs,
                       "all_citys": all_citys,
                       "org_nums": org_nums,
                       "city_id": city_id,
                       "category": category,
                       "hot_orgs": hot_orgs,
                       "sort": sort},
                      )


class AddUserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            # 异常方便的就存进来了
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"error","msg":"添加失败"}', content_type='application/json')


class OrgHomeView(View):
    """机构首页"""

    @staticmethod
    def get(request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        # Course 有 course_org 外键,可以这样取外键对应的所有course
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]

        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-homepage.html', {
            'all_course': all_courses,
            'all_teacher': all_teachers,
            'course_org': course_org,
            "current_page": "home",
            'has_fav': has_fav
        })


class OrgCourseView(View):
    """机构课程"""

    @staticmethod
    def get(request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        # Course 有 course_org 外键,可以这样取外键对应的所有course
        all_courses = course_org.course_set.all()

        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-course.html', {
            'all_course': all_courses,
            'course_org': course_org,
            "current_page": "course",
            'has_fav': has_fav
        })


class OrgDescView(View):
    """机构介绍"""

    @staticmethod
    def get(request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        # Course 有 course_org 外键,可以这样取外键对应的所有course
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            "current_page": "desc",
            'has_fav': has_fav
        })


class OrgTeacherView(View):
    """机构讲师介绍"""

    @staticmethod
    def get(request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        # Course 有 course_org 外键,可以这样取外键对应的所有course
        all_teachers = course_org.teacher_set.all()

        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-teachers.html', {
            'all_teacher': all_teachers,
            'course_org': course_org,
            "current_page": "teacher",
            'has_fav': has_fav
        })


class AddFavView(View):
    """用户收藏取消收藏"""

    @staticmethod
    def post(request):
        fav_id = int(request.POST.get("fav_id")) if request.POST.get("fav_id") else None
        fav_type = int(request.POST.get("fav_type")) if request.POST.get("fav_type") else None

        if not request.user.is_authenticated:  # 用户没登录
            return HttpResponse('{"status":"error","msg":"用户未登录"}', content_type='application/json')
        elif fav_id and fav_type:
            exist_records = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
            if exist_records:
                exist_records.delete()
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    if course.fav_nums >=1:
                        course.fav_nums -= 1
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    if course_org.fav_nums >= 1:
                        course_org.fav_nums -= 1
                    course_org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    if teacher.fav_nums >= 1:
                        teacher.fav_nuns -= 1
                    teacher.save()
                return HttpResponse('{"status":"success","msg":"收藏"}', content_type='application/json')
            else:
                UserFavorite.objects.create(user=request.user, fav_id=fav_id, fav_type=fav_type)
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nuns += 1
                    teacher.save()
                return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"error","msg":"收藏出错"}', content_type='application/json')


# 课程讲师列表页
class TeacherListView(View):
    def get(self, request):
        all_teacher = Teacher.objects.all()
        sort = request.GET.get("sort", "")
        if sort:
            if sort == "hot":
                all_teacher = all_teacher.order_by("-click_nums")

        # 搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # 在name字段进行操作,做like语句的操作。i代表不区分大小写
            # or操作使用Q
            all_teacher = all_teacher.filter(
                Q(name__icontains=search_keywords) | Q(work_company__icontains=search_keywords))

        # 排行榜讲师
        rank_teacher = Teacher.objects.all().order_by("-fav_nums")[:5]
        # 总共有多少老师使用count进行统计
        teacher_nums = all_teacher.count()
        # 对讲师进行分页
        # 尝试获取前台get请求传递过来的page参数
        # 如果是不合法的配置参数默认返回第一页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 这里指从allorg中取五个出来，每页显示5个
        p = Paginator(all_teacher, 4, request=request)
        teachers = p.page(page)
        return render(request, "teachers-list.html", {
            "all_teacher": teachers,
            "teacher_nums": teacher_nums,
            "sort": sort,
            "rank_teachers": rank_teacher,
            "search_keywords": search_keywords,
            "current_nav": "teacher"
        })


# 教师详情页面

class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums += 1
        teacher.save()
        all_course = teacher.course_set.all()
        # 排行榜讲师
        rank_teacher = Teacher.objects.all().order_by("-fav_nums")[:5]

        has_fav_teacher = False
        if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
            has_fav_teacher = True
        has_fav_org = False
        if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
            has_fav_org = True
        return render(request, "teacher-detail.html", {
            "teacher": teacher,
            "all_course": all_course,
            "rank_teacher": rank_teacher,
            "has_fav_teacher": has_fav_teacher,
            "has_fav_org": has_fav_org,
        })
