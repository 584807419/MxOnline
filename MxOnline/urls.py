"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from MxOnline.settings import MEDIA_ROOT

import xadmin

from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView, LogoutView, \
    IndexView
from organization.views import OrgView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('', IndexView.as_view(), name="index"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name="register"),
    path('captcha/', include('captcha.urls')),
    re_path('active/(?P<active_code>.*)/', ActiveUserView.as_view(), name="user_activate"),
    path('forget/', ForgetPwdView.as_view(), name="forget_pwd"),
    re_path('reset/(?P<active_code>.*)/', ResetView.as_view(), name="reset_pwd"),
    path('modify_pwd/', ModifyPwdView.as_view(), name="modify_pwd"),
    # 课程机构url配置
    re_path('org/', include(('organization.urls', 'organization'), namespace="org")),

    # 课程相关url配置
    re_path('course/', include(('courses.urls', 'courses'), namespace="course")),
    re_path('teacher/', include(('organization.urls', 'organization'), namespace="teacher")),
    re_path(r'media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),  # 配置上传文件的访问处理函数
    # re_path(r'static/(?P<path>.*)', serve, {"document_root": STATIC_ROOT}),  # 自己管理静态文件
    # 用户个人中心
    path('users/', include(('users.urls', 'users'), namespace="users")),

]

handler404 = 'users.views.page_not_found'
handler500 = "users.views.page_error"
