from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password

import re
from django.contrib.auth.models import User, Group

from .forms import AuthForms, ClassAddForms, ScheduleAddForms, UserAddForms, HomeWorkForms, LessonAddForms, \
    UserImageForm, UserEditForms, ClassStudentsAddForms
from .models import Day, SchoolClass, Lesson, Schedule, HomeWork, UserImage, Teacher

classes = SchoolClass.objects.all()

titles = [classes_.title for classes_ in classes]


def get_data(handler):
    username = handler.cleaned_data['username']
    password = handler.cleaned_data['password']
    first_name = handler.cleaned_data['first_name']
    last_name = handler.cleaned_data['last_name']
    email = handler.cleaned_data['email']

    group = handler.cleaned_data['group']
    groups = Group.objects.get(name=group)

    return {'username': username, 'password': password, 'first_name': first_name, 'last_name': last_name,
            'email': email,
            'group': group, 'groups': groups}


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
            day = form.cleaned_data['day']  # object

            schoolclass = SchoolClass.objects.filter(title=class_title).first()

            lesson = form.cleaned_data['lesson']
            lessonteacher = form.cleaned_data['lessonteacher']

            date = form.cleaned_data['date']

            start = form.cleaned_data['start']
            end = form.cleaned_data['end']

            new_schedule = Schedule(day=day, schoolclass=schoolclass, lesson=lesson, lessonteacher=lessonteacher ,date=date,
                                    start=start, end=end)
            new_schedule.save()

            return redirect('class_schedule', class_title, 'September', '1-7')

    else:
        if request.user.groups.get().name == 'Student' and request.user.schoolclass_set.first().title != class_title:
            return redirect('class_schedule', request.user.schoolclass_set.first().title, 'September', '1-7')

        schoolclass = SchoolClass.objects.filter(title=class_title).first()
        all_schedules = Schedule.objects.filter(schoolclass=schoolclass).all().order_by('start')

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
    schoolclasses = SchoolClass.objects.all()
    addforms = ClassAddForms()
    if request.user.groups.values_list('name', flat=True).first() != 'Admin':
        return redirect('index')
    elif request.method == 'GET':

        return render(request, 'Journal/classes.html', {'titles': sorted_titles,
                                                        'schoolclasses': schoolclasses, 'addforms': addforms})
    else:
        form = ClassAddForms(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']

            new_class = SchoolClass(title=title)
            new_class.save()

            success = True
            return render(request, 'Journal/classes.html', {'titles': sorted_titles,
                                                            'schoolclasses': schoolclasses, 'addforms': addforms,
                                                            'success': success})

        error = True
        return render(request, 'Journal/classes.html', {'titles': sorted_titles,
                                                        'schoolclasses': schoolclasses, 'addforms': addforms,
                                                        'error': error})


@login_required(login_url='/login')
def thisclass(request, class_id):
    curr_class = SchoolClass.objects.filter(id=class_id).first()

    if request.method == 'GET':
        forms = ClassStudentsAddForms()
        curr_class_students = curr_class.students.all()

        return render(request, 'Journal/thisclass.html', {'forms': forms, 'curr_class': curr_class,
                                                          'students': curr_class_students})

    else:
        forms = ClassStudentsAddForms(request.POST)
        if forms.is_valid():
            students_id = forms.data.getlist('students')

            for student_id in students_id:
                curr_class.students.add(student_id)

            curr_class.save()

            return redirect('thisclass', curr_class.id)


@login_required(login_url="/login/")
def class_delete(request, class_title):
    if request.user.groups.values_list('name', flat=True).first() != 'Admin':
        return redirect('index')
    c = SchoolClass.objects.filter(title=class_title).first()
    c.delete()

    return redirect('classes')


@login_required(login_url="/login/")
def users(request):
    users = User.objects.all()

    forms = UserAddForms()
    image_form = UserImageForm()

    if request.user.groups.values_list('name', flat=True).first() != 'Admin':
        return redirect('index')
    elif request.method == 'GET':
        return render(request, 'Journal/users.html', {'users': users, 'forms': forms, 'image_form': image_form})
    else:
        forms_post = UserAddForms(request.POST)
        image_form = UserImageForm(request.POST, request.FILES)
        if forms_post.is_valid() and image_form.is_valid():

            data = get_data(forms_post)

            new_user = User.objects.create_user(username=data['username'],
                                                password=data['password'],
                                                first_name=data['first_name'],
                                                last_name=data['last_name'],
                                                email=data['email'])

            new_user.save()
            data['groups'].user_set.add(new_user)

            if image_form.cleaned_data['image'] is not None:

                image = image_form.save(commit=False)
                image.user = new_user
                image.save()

            success = True
            return render(request, 'Journal/users.html', {'users': users, 'forms': forms_post, 'success': success,
                                                          'image_form': image_form})
        else:

            error = True
            return render(request, 'Journal/users.html', {'users': users, 'forms': forms_post, 'error': error,
                                                          'image_form': image_form})


@login_required(login_url='/login/')
def lessons(request):
    lessons = Lesson.objects.all()
    lessonsforms = LessonAddForms()
    if request.user.groups.values_list('name', flat=True).first() != 'Admin':
        return redirect('index')
    elif request.method == 'GET':

        return render(request, 'Journal/lessons.html', {'titles': sorted_titles,
                                                        'lessons': lessons, 'lessonsforms': lessonsforms})
    else:
        form = LessonAddForms(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']

            new_lesson = Lesson(title=title)
            new_lesson.save()

            success = True
            return render(request, 'Journal/lessons.html', {'titles': sorted_titles,
                                                            'lessons': lessons, 'lessonsforms': lessonsforms,
                                                            'success': success})

        error = True
        return render(request, 'Journal/lessons.html', {'titles': sorted_titles,
                                                        'lessons': lessons, 'lessonsforms': lessonsforms,
                                                        'error': error})


@login_required(login_url='/login/')
def homework(request):
    teacher = Teacher.objects.filter(user=request.user).first()

    forms = HomeWorkForms()
    forms.fields['schedule'].queryset = Schedule.objects.filter(homework=None).filter(lessonteacher=teacher)

    if teacher is None:
        myhomeworks = None
    else:
        myhomeworks = teacher.schedule_set.all()

    if request.method == 'GET':
        return render(request, 'Journal/homework.html', {'forms': forms, 'myhomeworks': myhomeworks})
    else:
        forms_post = HomeWorkForms(request.POST)
        if forms_post.is_valid():
            schedule = forms_post.cleaned_data['schedule']
            text = forms_post.cleaned_data['text']

            new_homework = HomeWork(schedule=schedule, text=text)
            new_homework.save()

            success = True
            return render(request, 'Journal/homework.html',
                          {'forms': forms, 'success': success, 'myhomeworks': myhomeworks})
        else:
            error = True
            return render(request, 'Journal/homework.html', {'forms': forms, 'error': error, 'myhomeworks': myhomeworks})


@login_required(login_url='/login/')
def profile(request, user_id):
    curr_user = User.objects.filter(id=user_id).first()
    user_image = UserImage.objects.filter(user=curr_user).first()
    image_form = UserImageForm()

    if user_image is None:
        profile_photo = 1
    else:
        profile_photo = user_image.image.url

    if request.method == 'GET':
        user_form = UserEditForms(initial={'username': curr_user.username, 'password': curr_user.password,
                                           'first_name': curr_user.first_name, 'last_name': curr_user.last_name,
                                           'email': curr_user.email, 'group': curr_user.groups.first().name,
                                           })

        #teacher_form = TeacherForm()

        return render(request, 'Journal/profile.html', {'profile_photo': profile_photo, 'curr_user': curr_user,
                                                        'image_form': image_form, 'user_form': user_form,
                                                        })

    else:  # POST
        user_form = UserEditForms(request.POST)
        image_form = UserImageForm(request.POST, request.FILES)
        #teacher_form = TeacherForm(request.POST)
        if image_form.is_valid() and user_form.is_valid(): #and teacher_form.is_valid():
            # schoolclasses = teacher_form['schoolclasses']
            # lessons = teacher_form['lessons']

            # teacher = teacher_form.save(commit=False)
            #
            # teacher = Teacher.objects.create(
            #     user=curr_user
            # )
            #
            # teacher.schoolclasses.add(schoolclasses)
            # teacher.lessons.add(lessons)

            image = image_form.cleaned_data['image']

            if image != None:

                user_image = UserImage.objects.filter(user=curr_user).first()

                if user_image is not None:
                    user_image.image.delete()
                    user_image.delete()

                    image = image_form.save(commit=False)
                    image.user = curr_user

                    image.save()

                    return redirect('profile', curr_user.id)

                else:
                    image = image_form.save(commit=False)
                    image.user = curr_user

                    image.save()

            data = get_data(user_form)

            curr_user.username = data['username']

            curr_user.first_name = data['first_name']

            curr_user.last_name = data['last_name']
            curr_user.email = data['email']


            curr_user.save()
            data['groups'].user_set.remove(curr_user)
            data['groups'].user_set.add(curr_user)

            if not check_password(data['password'], curr_user.password):
                curr_user.set_password(data['password'])
                curr_user.save()

            return redirect('profile', curr_user.id)
        else:
            error = True
            return render(request, 'Journal/profile.html', {'profile_photo': profile_photo, 'curr_user': curr_user,
                                                            'image_form': image_form, 'user_form': user_form,
                                                            'error': error})


@login_required(login_url='/login/')
def user_delete(request, user_id):
    u = User.objects.filter(id=user_id).first()
    user_image = UserImage.objects.filter(user=u).first()

    user_image.image.delete()
    user_image.delete()

    u.delete()

    return redirect('users')


def logout_view(request):
    logout(request)
    return redirect('index')