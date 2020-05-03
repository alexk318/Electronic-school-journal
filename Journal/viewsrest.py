from .models import Schedule
from .serializers import ScheduleSerializer, StudentsSerializer

from django.contrib.auth.models import User, Group

from rest_framework.response import Response
from rest_framework.views import APIView

# Get all Lessons


class ScheduleView(APIView):
    def get(self, request):
        all_schedules = Schedule.objects.all()
        serializer = ScheduleSerializer(all_schedules, many=True)

        return Response({"all_schedules": serializer.data})


student = Group.objects.get(name='Student')


class StudentsView(APIView):
    def get(self, request):
        all_students = User.objects.filter(groups=student).all()
        serializer = StudentsSerializer(all_students, many=True)

        return Response({"all_students": serializer.data})

    def post(self, request):
        student = request.data.get('student')

        serializer = StudentsSerializer(data=student)

        if serializer.is_valid(raise_exception=True):
            student_saved = serializer.save()

        return Response({"success": "Student '{} {}' create successfully".format(student_saved.first_name,
                                                                                 student_saved.last_name)})
