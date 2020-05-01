from .models import Lesson
from .serializers import LessonSerializer

from rest_framework.response import Response
from rest_framework.views import APIView

# Get all Lessons


class LessonView(APIView):
    def get(self, request):
        all_lessons = Lesson.objects.all()
        serializer = LessonSerializer(all_lessons, many=True)

        return Response({"all_lessons": serializer.data})


