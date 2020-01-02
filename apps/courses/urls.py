from django.conf.urls import url

from courses.views import CourseListView, CourseDescView, CourseInfoView, CourseCommentView, AddCommentView

urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
    url(r'^desc/(?P<course_id>\d+)/$', CourseDescView.as_view(), name='course_desc'),
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='course_info'),
    url(r'^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name='course_comment'),
    url(r'^add_comment/$', AddCommentView.as_view(), name='add_comment'),
]
