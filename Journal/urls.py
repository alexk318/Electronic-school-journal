from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.log_in, name='login'),

    path('journal/', views.journal, name='journal'),
    path('journal/schedule/', views.schedule, name='schedule'),

    path('journal/classes/', views.classes, name='classes'),
    path('journal/classes/add/', views.class_add, name='class_add'),
    path('journal/classes/delete/<class_title>', views.class_delete, name='class_delete'),

    path('logout/', views.logout_view, name='logout'),
]
