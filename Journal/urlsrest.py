from django.urls import path

from .viewsrest import StudentListView, StudentCreateView, StudentDetailView

app_name = 'territory'

urlpatterns = [
    # add, delete, update и т.д. является хорошим решением, а не анти-паттерном

    path('student/detail/<int:pk>/', StudentDetailView.as_view()),
    path('student/list/', StudentListView.as_view()),
    path('student/create/', StudentCreateView.as_view()),
]