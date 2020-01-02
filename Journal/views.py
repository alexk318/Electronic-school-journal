from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login

import re

from .forms import AuthForms, ClassAddForms
from .models import SchoolClass, Schedule, Day


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
        all_schoolclasses = SchoolClass.objects.all()

        return render(request, 'Journal/schedule.html', {'titles': sorted_titles})
    else:
        return redirect('index')


def class_schedule(request, class_title):
    if request.user.groups.values_list('name', flat=True).first() == 'Admin':
        monday = Day.objects.filter(title='Monday').first()
        tuesday = Day.objects.filter(title='Tuesday').first()
        wednesday = Day.objects.filter(title='Wednesday').first()
        thursday = Day.objects.filter(title='Thursday').first()
        friday = Day.objects.filter(title='Friday').first()


        schoolclass = SchoolClass.objects.filter(title=class_title).first()

        schedule_monday = Schedule.objects.filter(schoolclass=schoolclass, day=monday).first()
        schedule_tuesday = Schedule.objects.filter(schoolclass=schoolclass, day=tuesday).first()
        schedule_wednesday = Schedule.objects.filter(schoolclass=schoolclass, day=wednesday).first()
        schedule_thursday = Schedule.objects.filter(schoolclass=schoolclass, day=thursday).first()
        schedule_friday = Schedule.objects.filter(schoolclass=schoolclass, day=friday).first()

        lessons_monday = schedule_monday.lesson.all()
        lessons_tuesday = schedule_tuesday.lesson.all()
        lessons_wednesday = schedule_wednesday.lesson.all()
        lessons_thursday = schedule_thursday.lesson.all()
        lessons_friday = schedule_friday.lesson.all()


        return render(request, 'Journal/schedule.html', {'titles': titles,
                                                         'class_title': class_title,
                                                         'schedule': schedule,

                                                         'lessons_monday': lessons_monday,
                                                         'lessons_tuesday': lessons_tuesday,
                                                         'lessons_wednesday': lessons_wednesday,
                                                         'lessons_thursday': lessons_thursday,
                                                         'lessons_friday': lessons_friday,
                                                         })
    else:
        return redirect('index')





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
