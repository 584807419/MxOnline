from courses.views import CourseListView, CourseDetailView, CourseInfoView, CommentsView, AddCommentsView, VideoPlayView
from django.urls import path, re_path

from .views import UserInfoView

app_name = "courses"
urlpatterns = [
    # 用户信息
    path('info/', UserInfoView.as_view(), name="user_info"),
    path('image/upload/', UserInfoView.as_view(), name="image_upload"),

]
