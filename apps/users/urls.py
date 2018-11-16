from courses.views import CourseListView, CourseDetailView, CourseInfoView, CommentsView, AddCommentsView, VideoPlayView
from django.urls import path, re_path

from .views import UserInfoView, UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView

app_name = "users"
urlpatterns = [
    # 用户信息
    path('info/', UserInfoView.as_view(), name="user_info"),
    path('image/upload/', UploadImageView.as_view(), name="image_upload"),
    path('update/pwd/', UpdatePwdView.as_view(), name="update_pwd"),
    path('sendemail_code/', SendEmailCodeView.as_view(), name="sendemail_code"),
    path('update_email/', UpdateEmailView.as_view(), name="update_email"),
path('image/uploadw/', UserInfoView.as_view(), name="mycourse"),
path('image/uploadw/', UserInfoView.as_view(), name="my_message"),
path('image/uploade/', UserInfoView.as_view(), name="myfav_org"),
]
