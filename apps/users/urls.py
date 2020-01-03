from django.conf.urls import url

from users.views import UserInfoView

urlpatterns = [
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),
]
