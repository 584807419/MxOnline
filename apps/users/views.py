import json

from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm, UserInfoForm

from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin

from operation.models import UserCourse


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# Create your views here.

class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return render(request, "index.html", {})
                else:
                    return render(request, 'login.html', {"msg": "用户没有激活"})
            else:
                return render(request, "login.html", {"msg": "用户名密码错误"})
        else:
            return render(request, "login.html", {"login_form": login_form})


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {"register_form": register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email")
            pass_word = request.POST.get("password")
            if user_name:
                if UserProfile.objects.filter(email=user_name):
                    return render(request, "register.html", {"register_form": register_form, "msg": "邮箱已存在"})
            UserProfile.objects.get_or_create(username=user_name, email=user_name, password=make_password(pass_word),
                                              is_active=False)

            send_register_email(user_name, "register")

            return render(request, "login.html")
        else:
            return render(request, "register.html", {"register_form": register_form})


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.update_fields(is_active=True)
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email")
            send_register_email(email, "forget")
            return render(request, "send_success.html", {})
        else:
            return render(request, 'forgetpwd.html', {"forget_form": forget_form})


class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email": email})
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1")
            pwd2 = request.POST.get("password2")
            email = request.POST.get("email")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email, "msg": "密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.update_fields(password=make_password(pwd2))
            return render(request, 'login.html')
        else:
            return render(request, "password_reset.html",
                          {"email": request.POST.get("email"), "modify_form": modify_form})


class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        """用户个人信息"""
        return render(request, 'usercenter-info.html', {})

    def post(self, request):
        # 使用from的时候要注意,如果不指定instance,那么save的时候会认为新增一个,而不是修改原有的
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type="application/json")
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type="application/json")


class UploadImageView(LoginRequiredMixin, View):
    """用户修改头像"""

    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type="application/json")
        else:
            return HttpResponse('{"status":"error"}', content_type="application/json")


class UpdatePwdView(LoginRequiredMixin, View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1")
            pwd2 = request.POST.get("password2")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"error","msg":"密码不一致"}', content_type="application/json")
            user = request.user
            user.update_fields(password=make_password(pwd2))
            return HttpResponse('{"status":"success"}', content_type="application/json")
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type="application/json")


class SendEmailCodeView(LoginRequiredMixin, View):
    def get(self, request):
        email = request.GET.get('email', "")
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"status":"error", "msg":"邮箱已经被使用"}', content_type="application/json")
        send_register_email(email, "update_email")
        return HttpResponse('{"status":"success"}', content_type="application/json")


class UpdateEmailView(LoginRequiredMixin, View):
    def post(self, request):
        email = request.POST.get("email", "")
        code = request.POST.get("code", "")
        existed_recored = EmailVerifyRecord.objects.filter(email=email, code=code, send_type="update_email")
        if existed_recored:
            request.user.email = email
            request.user.save()
            return HttpResponse('{"status":"success"}', content_type="application/json")
        else:
            return HttpResponse('{"status":"error","msg":"验证码错误"}', content_type="application/json")


class MyCourseView(LoginRequiredMixin, View):
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {"user_courses": user_courses})
