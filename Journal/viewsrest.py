from .models import Schedule
from .serializers import ScheduleSerializer

from rest_framework.response import Response
from rest_framework.views import APIView

# Get all Lessons


class ScheduleView(APIView):
    def get(self, request):
        all_schedules = Schedule.objects.all()
        serializer = ScheduleSerializer(all_schedules, many=True)

        return Response({"all_schedules": serializer.data})


