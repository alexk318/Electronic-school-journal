import datetime

from django import template
from Journal.models import Schedule

register = template.Library()


@register.simple_tag
def get_curruser_newhomeworks(request):
    student_schedules = Schedule.objects.filter(schoolclass=request.user.schoolclass_set.first()).all()
    homeworks = [s.homework_set.first() for s in student_schedules if s.homework_set.first() is not None]

    return len(homeworks)


now = datetime.datetime.now()


@register.simple_tag
def get_current_month():
    current_month = now.strftime('%B')

    return current_month


@register.simple_tag
def get_current_week():
    current_day = now.day

    week1 = (1, 2, 3, 4, 5, 6, 7)
    week2 = (8, 9, 10, 11, 12, 13, 14)
    week3 = (15, 16, 17, 18, 19, 20, 21)
    week4 = (22, 23, 24, 25, 26, 27, 28)
    week5 = (29, 30, 31)

    if current_day in week1:
        current_week = '1-7'
    elif current_day in week2:
        current_week = '8-14'
    elif current_day in week3:
        current_week = '15-21'
    elif current_day in week4:
        current_week = '22-28'
    elif current_day in week5:
        current_week = '29-31'
    else:
        current_week = 'error'

    return current_week
