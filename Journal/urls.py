from django.urls import path
from JournalBase import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.log_in, name='login'),

    path('journal/profile/<int:user_id>', views.profile, name='profile'),

    path('journal/', views.journal, name='journal'),
    path('journal/schedule/', views.schedule, name='schedule'),

    path('journal/schedule/<str:class_title>/<str:month_title>/<str:week_numbers>', views.class_schedule,
         name='class_schedule'),

    path('journal/classes/', views.classes, name='classes'),
    path('journal/classes/delete/<class_title>', views.class_delete, name='class_delete'),

    path('journal/users/', views.users, name='users'),

    path('journal/lessons/', views.lessons, name='lessons'),

    path('journal/homework', views.homework, name='homework'),

    path('logout/', views.logout_view, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

