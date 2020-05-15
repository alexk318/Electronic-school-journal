from django.urls import path

from .viewsrest import UserListView, UserCreateView, UserDetailView, GradeListView, GradeDetailView, GradeCreateView, \
    TeacherCreateView, TeacherDetailView, TeacherListView, SchoolClassCreateView, SchoolClassDetailView, \
    SchoolClassListView, DayCreateView, DayDetailView, DayListView, LessonListView, LessonCreateView, LessonDetailView,\
    ScheduleCreateView, ScheduleDetailView, ScheduleListView, HomeWorkCreateView, HomeWorkDetailView, HomeWorkListView,\
    IndividualHomeworkCreateView, IndividualHomeworkDetailView, IndividualHomeworkListView


urlpatterns = [
    path('grade/detail/<int:pk>/', GradeDetailView.as_view()),
    path('grades/list/', GradeListView.as_view()),
    path('grade/create/', GradeCreateView.as_view()),

    path('teacher/detail/<int:pk>/', TeacherDetailView.as_view()),
    path('teachers/list/', TeacherListView.as_view()),
    path('teacher/create/', TeacherCreateView.as_view()),

    path('schoolclass/detail/<int:pk>/', SchoolClassDetailView.as_view()),
    path('schoolclasses/list/', SchoolClassListView.as_view()),
    path('schoolclass/create/', SchoolClassCreateView.as_view()),

    path('day/detail/<int:pk>/', DayDetailView.as_view()),
    path('days/list/', DayListView.as_view()),
    path('day/create/', DayCreateView.as_view()),

    path('lesson/detail/<int:pk>/', LessonDetailView.as_view()),
    path('lessons/list/', LessonListView.as_view()),
    path('lesson/create/', LessonCreateView.as_view()),

    path('schedule/detail/<int:pk>/', ScheduleDetailView.as_view()),
    path('schedules/list/', ScheduleListView.as_view()),
    path('schedule/create/', ScheduleCreateView.as_view()),

    path('homework/detail/<int:pk>/', HomeWorkDetailView.as_view()),
    path('homeworks/list/', HomeWorkListView.as_view()),
    path('homework/create/', HomeWorkCreateView.as_view()),

    path('individualhomework/detail/<int:pk>/', IndividualHomeworkDetailView.as_view()),
    path('individualhomeworks/list/', IndividualHomeworkListView.as_view()),
    path('individualhomework/create/', IndividualHomeworkCreateView.as_view()),

    path('user/detail/<int:pk>/', UserDetailView.as_view()),
    path('users/list/', UserListView.as_view()),
    path('user/create/', UserCreateView.as_view()),
]
