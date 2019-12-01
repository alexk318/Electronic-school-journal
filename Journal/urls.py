from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('journal/', views.journal, name='journal'),
    path('logout/', views.logout_view, name='logout'),
]
