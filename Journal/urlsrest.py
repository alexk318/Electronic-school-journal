from django.urls import path

from .viewsrest import StudentListView, StudentCreateView, StudentDetailView

urlpatterns = [
    path('student/detail/<int:pk>/', StudentDetailView.as_view()),
    path('student/list/', StudentListView.as_view()),
    path('student/create/', StudentCreateView.as_view()),
]