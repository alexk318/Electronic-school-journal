from django.urls import path

from django.conf.urls.static import static

from . import views, viewsrest
from JournalBase import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.log_in, name='login'),

    path('journal/profile/<int:user_id>', views.profile, name='profile'),
    path('journal/profile/<int:user_id>/delete', views.user_delete, name='user_delete'),
    path('journal/profile/<int:user_id>/imagerotate', views.rotate_image, name='rotate_image'),

    path('journal/schedule/', views.schedule, name='schedule'),

    path('journal/schedule/<str:class_title>/<str:month_title>/<str:week_numbers>', views.class_schedule,
         name='class_schedule'),

    path('journal/classes/', views.classes, name='classes'),
    path('journal/classes/<int:class_id>/', views.thisclass, name='thisclass'),
    path('journal/classes/<int:class_id>/delete/', views.class_delete, name='class_delete'),

    path('journal/users/', views.users, name='users'),

    path('journal/lessons/', views.lessons, name='lessons'),

    path('journal/homework', views.homework, name='homework'),
    path(
        'journal/homework/assign/<int:ih_id>/<int:submithomework_id>/<int:homework_id>/<int:schoolclass_id>/'
        '<int:student_id>',
        views.assign_grade, name='assign_grade'),

    path('journal/homework/submit/<int:homework_id>', views.submit_homework, name='submit_homework'),

    path('journal/homework/check/<int:homework_id>', views.check_homework, name='check_homework'),

    path('journal/download/<str:filepath>/<str:filename>', views.download, name='download'),

    path('journal/homework/individual/<int:schoolclass_id>/<int:student_id>', views.individual_homework,
         name='individual_homework'),
    path('journal/homework/individual/submit/<int:individualhomework_id>', views.submit_individualhomework,
         name='submit_individualhomework'),

    path('journal/grades/', views.grades, name='grades'),

    path('journal/homework/close/<int:h_id>', views.close_homework, name='close_homework'),
    path('journal/homework/individual/close/<int:h_id>', views.close_individualhomework,
         name='close_individualhomework'),

    path('logout/', views.logout_view, name='logout'),


    path('api/schedule', viewsrest.ScheduleView.as_view()),
    path('api/students', viewsrest.StudentsView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
