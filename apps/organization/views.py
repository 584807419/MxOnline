from django.shortcuts import render
from django.views.generic import View
from .models import CourseOrg, CityDict

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.


class OrgView(View):
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        all_citys = CityDict.objects.all()

        # 取出筛选的城市
        city_id = request.GET.get("city")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))
        # 类别筛选
        category = request.GET.get("ct", "")
        if category:
            all_orgs = all_orgs.filter(category=category)
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
                       "category": category})
