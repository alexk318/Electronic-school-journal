from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login

import re
from datetime import datetime

from .forms import AuthForms, ClassAddForms
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


def journal(request):
    if request.user.is_authenticated:
        return render(request, 'Journal/journal.html', {'current_user': request.user,
                                                        'group': request.user.groups.values_list('name', flat=True).
                      first()})
    else:
        msg = 'To access the journal you need to log in!'
        forms = AuthForms()
        return render(request, 'Journal/index.html', {'forms': forms, 'msg': msg})


def schedule(request):
    if request.user.groups.values_list('name', flat=True).first() == 'Admin':
        return render(request, 'Journal/schedule.html', {'titles': sorted_titles})
    else:
        return redirect('index')


def class_schedule(request, class_title):
    if request.user.groups.values_list('name', flat=True).first() == 'Admin':
        schoolclass = SchoolClass.objects.filter(title=class_title).first()
        all_schedules = Schedule.objects.filter(schoolclass=schoolclass).all()

        days = Day.objects.all()
        lessons = Lesson.objects.all()

        schedules = []
        for i in all_schedules:
            date = i.date
            date_datetime = datetime.strptime(date, '%Y-%m-%d')
            month = int(date_datetime.strftime('%m'))

            if month == 2:
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

        return render(request, 'Journal/schedule.html', {'titles': sorted_titles,
                                                         'class_title': class_title,
                                                         'all_schedules': all_schedules,
                                                         'days': days,
                                                         'lessons': lessons,
                                                         'schedules_days': schedules_days,
                                                         })
    else:
        return redirect('index')


def schedule_add(request, day, class_title):
    schoolclass = SchoolClass.objects.filter(title=class_title).first()
    day = Day.objects.filter(title=day).first()

    lesson = Lesson.objects.filter(title=request.GET.get('lesson_selection')).first()
    date = request.GET.get('date_enter')

    new_schedule = Schedule(day=day, schoolclass=schoolclass, lesson=lesson, date=date)
    new_schedule.save()

    return redirect('class_schedule', class_title)

def classes(request):
    if request.user.groups.values_list('name', flat=True).first() != 'Admin':
        return redirect('index')
    else:

        addforms = ClassAddForms()
        return render(request, 'Journal/classes.html', {'titles': sorted_titles,
                                                        'classes': classes, 'addforms': addforms})


def class_add(request):
    form = ClassAddForms(request.POST)
    if form.is_valid():
        title = form.cleaned_data['title']

        new_class = SchoolClass(title=title)
        new_class.save()

    return redirect('classes')


def class_delete(request, class_title):
    if request.user.groups.values_list('name', flat=True).first() != 'Admin':
        return redirect('index')
    c = SchoolClass.objects.filter(title=class_title).first()
    c.delete()

    return redirect('classes')


def logout_view(request):
    logout(request)
    return redirect('index')
