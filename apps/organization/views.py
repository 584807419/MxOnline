from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from .models import CourseOrg, CityDict
from operation.models import UserFavorite
from .forms import UserAskForm

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.


class OrgView(View):
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        all_citys = CityDict.objects.all()
        # 热门机构
        hot_orgs = all_orgs.order_by("-click_nums")[:3]

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
                return HttpResponse('{"status":"success","msg":"收藏"}', content_type='application/json')
            else:
                UserFavorite.objects.create(user=request.user, fav_id=fav_id, fav_type=fav_type)
                return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"error","msg":"收藏出错"}', content_type='application/json')
