import json

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.shortcuts import render_to_response

from courses.models import Course
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from users.forms import LoginForm, RegisterForm, ForgetPwdForm, ResetPwdForm, UploadImageForm, UserInfoForm
from users.models import UserProfile, EmailVerifyRecord, Banner
from utils.send_email import send_email
from utils.login_required import LoginRequired
from pure_pagination import PageNotAnInteger, Paginator


def page_not_found(request, exception):
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response


class IndexView(View):
    def get(self, request):
        # 取出轮播图
        all_banners = Banner.objects.all().order_by('index')
        # 取出课程
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banners': all_banners,
            'courses': courses,
            'banner_courses': banner_courses,
            'course_orgs': course_orgs
        })


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        return render(request, 'register.html', {'register_form': register_form,
                                                 'banner_courses': banner_courses})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html',
                              {'msg': '用户已存在',
                               'register_form': register_form,
                               'banner_courses': banner_courses})
            password = request.POST.get('password', '')
            re_password = request.POST.get('re_password', '')
            nick_name = request.POST.get('nick_name', '')
            if password == re_password:
                user_profile = UserProfile()
                user_profile.username = user_name
                user_profile.email = user_name
                user_profile.password = make_password(password)
                user_profile.is_active = False
                user_profile.nick_name = nick_name
                user_profile.save()

                user_message = UserMessage()
                user_message.user = user_profile.id
                user_message.message = '欢迎注册'
                user_message.save()

                if send_email(user_name, 'register'):
                    return render(request, 'send_success.html')
            else:
                return render(request, 'register.html', {
                    'msg': '两次输入的密码不一致',
                    'banner_courses': banner_courses,
                    'register_form': register_form,
                })
        else:
            return render(request, 'register.html', {'register_form': register_form,
                                                     'banner_courses': banner_courses})


class LoginView(View):
    def get(self, request):
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        return render(request, 'login.html', {
            'banner_courses': banner_courses,
        })

    def post(self, request):
        login_form = LoginForm(request.POST)
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'msg': '账户未激活',
                                                          'banner_courses': banner_courses})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误',
                                                      'banner_courses': banner_courses})
        else:
            return render(request, 'login.html', {'login_form': login_form,
                                                  'banner_courses': banner_courses})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        email = ''
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return request(request, 'active_fail.html')
        request.session['email'] = email
        return redirect('login')


class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return request(request, 'active_fail.html')
        return render(request, 'login.html')


class ModifyPwdView(View):
    def post(self, request):
        reset_pwd_form = ResetPwdForm(request.POST)
        if reset_pwd_form.is_valid():
            pwd = request.POST.get('password')
            re_pwd = request.POST.get('re_password')
            email = request.POST.get('email')
            if pwd != re_pwd:
                return render(request, 'password_reset.html', {'email': email, 'msg': '密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd)
            user.save()
            return render(request, 'login.html')
        else:
            email = request.POST.get('email')
            return render(request, 'password_reset.html', {'email': email, 'reset_pwd_form': reset_pwd_form})


class ForgetPwdView(View):
    def get(self, request):
        forget_pwd_form = ForgetPwdForm()
        return render(request, 'forgetpwd.html', {'forget_pwd_form': forget_pwd_form})

    def post(self, request):
        forget_pwd_form = ForgetPwdForm(request.POST)
        if forget_pwd_form.is_valid():
            email = request.POST.get('email')
            send_email(email, 'forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_pwd_form': forget_pwd_form})


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class UserInfoView(LoginRequired, View):
    def get(self, request):
        return render(request, 'usercenter-info.html', {

        })

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors, ensure_ascii=False), content_type='application/json')


class UploadImageView(LoginRequired, View):
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class UpdatePwdView(View):
    def post(self, request):
        reset_pwd_form = ResetPwdForm(request.POST)
        if reset_pwd_form.is_valid():
            pwd = request.POST.get('password')
            re_pwd = request.POST.get('re_password')
            if pwd != re_pwd:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd)
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"密码格式不对"}', content_type='application/json')


class SendEmailCodeView(LoginRequired, View):
    def get(self, request):
        email = request.GET.get('email', '')
        # 邮箱是否存在
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已被注册"}', content_type='application/json')
        send_email(email, 'update_email')
        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(LoginRequired, View):
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        existed_code = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if existed_code:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')


class MyCourseView(LoginRequired, View):
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            'user_courses': user_courses
        })


class MyFavOrgView(LoginRequired, View):
    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {
            'org_list': org_list
        })


class MyFavTeacherView(LoginRequired, View):
    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            'teacher_list': teacher_list
        })


class MyFavCourseView(LoginRequired, View):
    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
            'course_list': course_list
        })


class MyMessageView(LoginRequired, View):
    def get(self, request):
        all_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for message in all_messages:
            message.has_read = True
            message.save()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_messages, 5, request=request)
        messages = p.page(page)
        return render(request, 'usercenter-message.html', {
            'messages': messages
        })
