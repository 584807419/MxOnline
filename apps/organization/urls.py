from django.urls import path, include, re_path
from .views import OrgView,AddUserAskView

urlpatterns = [
    path('list/', OrgView.as_view(), name="org_list"),  # 课程机构首页
    path('add_ask/', AddUserAskView.as_view(), name="add_ask"),  # 提问
    path('home/(?P<org_id>\d+)', AddUserAskView.as_view(), name="add_ask"),  # 提问

]
