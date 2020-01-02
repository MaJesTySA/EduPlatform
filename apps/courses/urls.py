from django.conf.urls import url

from courses.views import CourseListView, CourseDescView, CourseInfoView

urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
    url(r'^desc/(?P<course_id>\d+)/$', CourseDescView.as_view(), name='course_desc'),
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='course_info'),
]
