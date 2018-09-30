from django.shortcuts import render
from django.views.generic import View
from .models import CourseOrg, CityDict
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

class userAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            # 异常方便的就存进来了
            user_ask = userask_form.save(commit=True)
