from django.urls import path, include, re_path
from .views import OrgView

urlpatterns = [
    path('list/', OrgView.as_view(), name="org_list"),  # 课程机构首页
    path('add_ask/', OrgView.as_view(), name="org_list"),  # 课程机构首页

]
