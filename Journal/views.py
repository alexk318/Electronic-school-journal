from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required

import re
import datetime
import time

from .forms import AuthForms, ClassAddForms, ScheduleAddForms
from .models import Day, SchoolClass, Lesson, Schedule

classes = SchoolClass.objects.all()
titles = [classes_.title for classes_ in classes]


def key(s):
    num, letters = re.match(r'(\d*)(.*)', s).groups()
    return float(num or 'inf'), letters


sorted_titles = sorted(titles, key=key)


def index(request):
    if request.user.is_authenticated:
        return redirect('journal')
    return render(request, 'Journal/index.html')


def log_in(request):
    if request.method == 'GET':
        forms = AuthForms()
        return render(request, 'Journal/login.html', {'forms': forms})
    else:
        forms = AuthForms(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('journal')
            else:
                msg = 'The entered data is incorrect'
                return render(request, 'Journal/login.html', {'forms': forms, 'msg': msg})


@login_required(login_url="/login/")
def journal(request):
    return render(request, 'Journal/journal.html', {'current_user': request.user,
                                                    'group': request.user.groups.values_list('name', flat=True).
                  first()})


@login_required(login_url="/login/")
def schedule(request):
    if request.method == 'GET':
        if request.user.groups.values_list('name', flat=True).first() == 'Admin':
            return render(request, 'Journal/schedule.html', {'titles': sorted_titles})
        else:
            return redirect('index')


@login_required(login_url="/login/")
def class_schedule(request, class_title, month_title, week_numbers):
    if request.method == 'POST':
        form = ScheduleAddForms(request.POST)

        if form.is_valid():
            day_title = form.cleaned_data['day_week']
            day = Day.objects.filter(title=day_title).first()

            schoolclass = SchoolClass.objects.filter(title=class_title).first()

            lesson_title = form.cleaned_data['lesson']
            lesson = Lesson.objects.filter(title=lesson_title).first()

            date = form.cleaned_data['lesson_date']

            start = form.cleaned_data['lesson_start']
            end = form.cleaned_data['lesson_end']

            new_schedule = Schedule(day=day, schoolclass=schoolclass, lesson=lesson, date=date,
                                    start=start, end=end)
            new_schedule.save()

            return redirect('class_schedule', class_title, 'September', '1-7')

    else:
        if request.user.groups.get().name == 'Student' and request.user.schoolclass_set.first().title != class_title:
            return redirect('class_schedule', request.user.schoolclass_set.first().title, 'September', '1-7')

        schoolclass = SchoolClass.objects.filter(title=class_title).first()
        all_schedules = Schedule.objects.filter(schoolclass=schoolclass).all()

        days = Day.objects.all()
        lessons = Lesson.objects.all()

        months = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'Jule': 7, 'August': 8,
                  'September': 9, 'October': 10, 'November': 11, 'December': 12}

        weeks = {'1-7': [1, 2, 3, 4, 5, 6, 7], '8-14': [8, 9, 10, 11, 12, 13, 14],
                 '15-21': [15, 16, 17, 18, 19, 20, 21], '22-28': [22, 23, 24, 25, 26, 27, 28], '29-31': [29, 30, 31]}

        schedules = []
        for i in all_schedules:
            date_datetime = i.date

            day = int(date_datetime.strftime('%d'))
            month = int(date_datetime.strftime('%m'))

            if month == months[month_title] and day in weeks[week_numbers]:
                schedules.append(i)

        schedules_monday = [s for s in schedules if s.day.title == 'Monday']
        schedules_tuesday = [s for s in schedules if s.day.title == 'Tuesday']
        schedules_wednesday = [s for s in schedules if s.day.title == 'Wednesday']
        schedules_thursday = [s for s in schedules if s.day.title == 'Thursday']
        schedules_friday = [s for s in schedules if s.day.title == 'Friday']

        schedules_days = list()
        schedules_days.append(schedules_monday)
        schedules_days.append(schedules_tuesday)
        schedules_days.append(schedules_wednesday)
        schedules_days.append(schedules_thursday)
        schedules_days.append(schedules_friday)

        form = ScheduleAddForms()

        return render(request, 'Journal/schedule.html', {'titles': sorted_titles,
                                                         'class_title': class_title,
                                                         'all_schedules': all_schedules,
                                                         'days': days,
                                                         'lessons': lessons,
                                                         'schedules_days': schedules_days,
                                                         'months': months,
                                                         'month_title': month_title,
                                                         'weeks': weeks,
                                                         'week_numbers': week_numbers,

                                                         'form': form,
                                                         })


@login_required(login_url="/login/")
def classes(request):
    if request.user.groups.values_list('name', flat=True).first() != 'Admin':
        return redirect('index')
    else:

        addforms = ClassAddForms()
        return render(request, 'Journal/classes.html', {'titles': sorted_titles,
                                                        'classes': classes, 'addforms': addforms})


@login_required(login_url="/login/")
def class_add(request):
    form = ClassAddForms(request.POST)
    if form.is_valid():
        title = form.cleaned_data['title']

        new_class = SchoolClass(title=title)
        new_class.save()

    return redirect('classes')


@login_required(login_url="/login/")
def class_delete(request, class_title):
    if request.user.groups.values_list('name', flat=True).first() != 'Admin':
        return redirect('index')
    c = SchoolClass.objects.filter(title=class_title).first()
    c.delete()

    return redirect('classes')


def logout_view(request):
    logout(request)
    return redirect('index')
