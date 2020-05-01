from django import template
from Journal.models import Schedule

register = template.Library()


@register.simple_tag
def get_curruser_newhomeworks(request):
    student_schedules = Schedule.objects.filter(schoolclass=request.user.schoolclass_set.first()).all()
    homeworks = [s.homework_set.first() for s in student_schedules if s.homework_set.first() is not None]

    return len(homeworks)
