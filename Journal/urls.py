from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.log_in, name='login'),

    path('journal/', views.journal, name='journal'),
    path('journal/schedule/', views.schedule, name='schedule'),

    path('journal/schedule/<str:class_title>/<str:month_title>/<str:week_numbers>', views.class_schedule,
         name='class_schedule'),

    path('journal/classes/', views.classes, name='classes'),
    path('journal/classes/delete/<class_title>', views.class_delete, name='class_delete'),

    path('journal/users/', views.users, name='users'),

    path('journal/homework', views.homework, name='homework'),

    path('logout/', views.logout_view, name='logout'),
]
