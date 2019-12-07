from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('journal/', views.journal, name='journal'),
    path('journal/schedule/', views.schedule, name='schedule'),
    path('logout/', views.logout_view, name='logout'),
]
