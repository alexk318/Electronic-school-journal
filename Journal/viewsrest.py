from .models import Schedule
from .serializers import *
from django.contrib.auth.models import User

from rest_framework import generics


class GradeListView(generics.ListAPIView):
    serializer_class = GradeSerializer
    queryset = Grade.objects.all()


class GradeCreateView(generics.CreateAPIView):
    serializer_class = GradeSerializer


class GradeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GradeSerializer
    queryset = Grade.objects.all()


class TeacherListView(generics.ListAPIView):
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()


class TeacherCreateView(generics.CreateAPIView):
    serializer_class = TeacherSerializer


class TeacherDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()


class SchoolClassListView(generics.ListAPIView):
    serializer_class = SchoolClassSerializer
    queryset = SchoolClass.objects.all()


class SchoolClassCreateView(generics.CreateAPIView):
    serializer_class = SchoolClassSerializer


class SchoolClassDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SchoolClassSerializer
    queryset = SchoolClass.objects.all()


class DayListView(generics.ListAPIView):
    serializer_class = DaySerialiizer
    queryset = Day.objects.all()


class DayCreateView(generics.CreateAPIView):
    serializer_class = DaySerialiizer


class DayDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DaySerialiizer
    queryset = Day.objects.all()


class LessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonCreateView(generics.CreateAPIView):
    serializer_class = LessonSerializer


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class ScheduleListView(generics.ListAPIView):
    serializer_class = ScheduleSerializer
    queryset = Schedule.objects.all()


class ScheduleCreateView(generics.CreateAPIView):
    serializer_class = LessonSerializer


class ScheduleDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ScheduleSerializer
    queryset = Schedule.objects.all()


class HomeWorkListView(generics.ListAPIView):
    serializer_class = HomeWorkSerializer
    queryset = HomeWork.objects.all()


class HomeWorkCreateView(generics.CreateAPIView):
    serializer_class = HomeWorkSerializer


class HomeWorkDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HomeWorkSerializer
    queryset = HomeWork.objects.all()


class IndividualHomeworkListView(generics.ListAPIView):
    serializer_class = IndividualHomeworkSerializer
    queryset = IndividualHomework.objects.all()


class IndividualHomeworkCreateView(generics.CreateAPIView):
    serializer_class = IndividualHomeworkSerializer


class IndividualHomeworkDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IndividualHomeworkSerializer
    queryset = IndividualHomework.objects.all()


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()



