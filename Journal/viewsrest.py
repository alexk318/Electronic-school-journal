from .models import Schedule
from .serializers import ScheduleSerializer, StudentSerializer

from django.contrib.auth.models import User, Group

from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

# Get all Lessons


class ScheduleView(APIView):
    def get(self, request):
        all_schedules = Schedule.objects.all()
        serializer = ScheduleSerializer(all_schedules, many=True)

        return Response({"all_schedules": serializer.data})


class StudentListView(generics.ListAPIView):
    serializer_class = StudentSerializer
    queryset = User.objects.filter(groups__name='Student')


class StudentCreateView(generics.CreateAPIView):
    serializer_class = StudentSerializer


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StudentSerializer
    queryset = User.objects.filter(groups__name='Student')
