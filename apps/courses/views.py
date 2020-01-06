from django.db.models import Q
from pure_pagination import PageNotAnInteger, Paginator
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from courses.models import Course, CourseResource, Video
from operation.models import UserFavorite, CourseComment, UserCourse
from utils.utils import LoginRequired


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')

        hot_courses = Course.objects.all().order_by('-click_nums')[:3]
        sort = request.GET.get('sort', '')

        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)|
                                             Q(desc__icontains=search_keywords)|
                                             Q(detail__icontains=search_keywords))

        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by('-students')
            elif sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 3, request=request)
        courses = p.page(page)
        return render(request, 'course-list.html', {
            'all_courses': courses,
            'sort': sort,
            'hot_courses': hot_courses
        })


class CourseDescView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()
        tag = course.tag

        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True
        if tag:
            related_courses = Course.objects.filter(tag=tag)[:1]
        else:
            related_courses = []
        return render(request, 'course-detail.html', {
            'course': course,
            'related_courses': related_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org
        })


class CourseInfoView(LoginRequired, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()
        is_learned = UserCourse.objects.filter(user=request.user, course=course)
        if not is_learned:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        all_resources = CourseResource.objects.filter(course=course)
        #从UserCourse中取出该课程的所有学习用户
        user_courses = UserCourse.objects.filter(course=course)
        #得到该课程的所有学习用户id
        user_ids = [user_course.user.id for user_course in user_courses]
        #根据所有学习用户的id得到他们的UserCourse对象
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        #根据UserCourse，从Course中得到课程的ID
        course_ids = [user_course.course.id for user_course in all_user_courses]
        #得到相关课程
        related_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]
        return render(request, 'course-video.html', {
            'course': course,
            'course_resources': all_resources,
            'related_courses': related_courses
        })


class CourseCommentView(LoginRequired, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComment.objects.filter(course=course).order_by("-id")
        return render(request, 'course-comment.html', {
            'course': course,
            'course_resources': all_resources,
            'all_comments': all_comments
        })


class AddCommentView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('{"status": "fail", "msg":"未登录"}',
                                content_type='application/json')
        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        if int(course_id) > 0 and comments:
            course_comment = CourseComment()
            course = Course.objects.get(id=int(course_id))
            course_comment.course = course
            course_comment.comments = comments
            course_comment.user = request.user
            course_comment.save()
            return HttpResponse('{"status": "success", "msg":"评论成功"}',
                                content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg":"评论失败"}',
                                content_type='application/json')


class VideoPlayView(View):
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        is_learned = UserCourse.objects.filter(user=request.user, course=course)
        if not is_learned:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        all_resources = CourseResource.objects.filter(course=course)
        #从UserCourse中取出该课程的所有学习用户
        user_courses = UserCourse.objects.filter(course=course)
        #得到该课程的所有学习用户id
        user_ids = [user_course.user.id for user_course in user_courses]
        #根据所有学习用户的id得到他们的UserCourse对象
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        #根据UserCourse，从Course中得到课程的ID
        course_ids = [user_course.course.id for user_course in all_user_courses]
        #得到相关课程
        related_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]
        return render(request, 'course-play.html', {
            'course': course,
            'course_resources': all_resources,
            'related_courses': related_courses,
            'video': video
        })
