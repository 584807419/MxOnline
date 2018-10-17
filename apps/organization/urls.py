from django.urls import path, include, re_path
from .views import OrgView, AddUserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, AddFavView, \
    TeacherListView, TeacherDetailView

urlpatterns = [
    path('list/', OrgView.as_view(), name="org_list"),  # 课程机构首页
    path('add_ask/', AddUserAskView.as_view(), name="add_ask"),  # 提问
    re_path('home/(?P<org_id>\d+)/', OrgHomeView.as_view(), name="org_home"),  # 机构主页
    re_path('course/(?P<org_id>\d+)/', OrgCourseView.as_view(), name="org_course"),  # 机构课程列表页
    re_path('desc/(?P<org_id>\d+)/', OrgDescView.as_view(), name="org_desc"),  # 机构介绍
    re_path('teacher/(?P<org_id>\d+)/', OrgTeacherView.as_view(), name="org_teacher"),  # 机构讲师介绍
    path('add_fav/', AddFavView.as_view(), name="add_fav"),  # 机构收藏
    # 讲师列表
    path('teacher/list/', TeacherListView.as_view(), name="teacher_list"),
    # 讲师详情
    re_path('teacher/detail/(?P<teacher_id>\d+)/', TeacherDetailView.as_view(), name="teacher_detail"),
]
