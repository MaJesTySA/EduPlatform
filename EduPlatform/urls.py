"""EduPlatform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls import url
import xadmin
from django.views.generic import TemplateView
from django.views.static import serve

from EduPlatform.settings import MEDIA_ROOT
from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ModifyPwdView, ResetView, LogoutView, \
    IndexView

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    url('^$', IndexView.as_view(), name='index'),
    url('^login/$', LoginView.as_view(), name='login'),
    url('^login(?P<email>.*)/$', LoginView.as_view(), name='login'),
    url('^logout/$', LogoutView.as_view(), name='logout'),
    url('^register/$', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    # 激活邮箱
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='user_active'),
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name='reset_pwd'),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name='modify_pwd'),
    url(r'^forget/$', ForgetPwdView.as_view(), name='forget_pwd'),
    # 课程机构
    url(r'^org/', include(('organization.urls', 'organization'), namespace='org')),
    # 课程详情
    url(r'^course/', include(('courses.urls', 'courses'), namespace='course')),
    url(r'^users/', include(('users.urls', 'users'), namespace='users')),
    # 上传文件的访问处理
    url(r'media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    # url(r'static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
]

handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'
