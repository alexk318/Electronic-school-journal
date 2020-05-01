from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User

import re
from django.utils.translation import ugettext as _

from .functions import get_data

from .forms import AuthForms, ClassAddForms, ScheduleAddForms, UserAddForms, HomeWorkForms, LessonAddForms, \
    UserImageForm, UserEditForms, ClassStudentsAddForms, GradesForms, IndividualHomeWorkForms
from .models import Day, SchoolClass, Lesson, Schedule, HomeWork, UserImage, Teacher, IndividualHomework, \
    SubmitHomework, Grade

classes = SchoolClass.objects.all()

titles = [classes_.title for classes_ in classes]


def key(s):
    num, letters = re.match(r'(\d*)(.*)', s).groups()
    return float(num or 'inf'), letters


sorted_titles = sorted(titles, key=key)

weeks = {'1-7': [1, 2, 3, 4, 5, 6, 7], '8-14': [8, 9, 10, 11, 12, 13, 14], '15-21': [15, 16, 17, 18, 19, 20, 21],
         '22-28': [22, 23, 24, 25, 26, 27, 28], '29-31': [29, 30, 31]}


def index(request):  # Getting started
    if request.user.is_authenticated:
        return redirect('homework')

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
                return redirect('schedule')
            else:
                msg = _('The entered data is incorrect')
                return render(request, 'Journal/login.html', {'forms': forms, 'msg': msg})
        else:
            msg = _('The entered data is incorrect')
            return render(request, 'Journal/login.html', {'forms': forms, 'msg': msg})


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

            date = request.POST['date']  # str: YYYY-MM-DD

            start = request.POST['start']  # str: HH:MM
            end = request.POST['end']

            new_schedule = Schedule(day=day, schoolclass=schoolclass, lesson=lesson, lessonteacher=lessonteacher,
                                    date=date,
                                    start=start, end=end)
            new_schedule.save()

            return redirect('class_schedule', class_title, 'September', '1-7')

    else:
        if request.user.groups.get().name == 'Student' and request.user.schoolclass_set.first().title != class_title:
            return redirect('class_schedule', request.user.schoolclass_set.first().title, 'September', '1-7')

        schoolclass = SchoolClass.objects.filter(title=class_title).first()
        all_schedules = Schedule.objects.filter(schoolclass=schoolclass).all().order_by('start')

        days = Day.objects.all()
        alllessons = Lesson.objects.all()

        months = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'Jule': 7, 'August': 8,
                  'September': 9, 'October': 10, 'November': 11, 'December': 12}

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
                                                         'lessons': alllessons,
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
def class_delete(request, class_id):
    if request.user.groups.values_list('name', flat=True).first() != 'Admin':
        return redirect('index')
    c = SchoolClass.objects.filter(id=class_id).first()
    c.delete()

    return redirect('classes')


@login_required(login_url="/login/")
def users(request):
    allusers = User.objects.all()

    forms = UserAddForms()
    image_form = UserImageForm()

    if request.user.groups.values_list('name', flat=True).first() != 'Admin':
        return redirect('index')
    elif request.method == 'GET':
        return render(request, 'Journal/users.html', {'users': allusers, 'forms': forms, 'image_form': image_form})
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

            if data['groups'].name == 'Teacher':
                t = Teacher(user=new_user)
                t.save()

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
    alllessons = Lesson.objects.all()
    lessonsforms = LessonAddForms()
    if request.user.groups.values_list('name', flat=True).first() != 'Admin':
        return redirect('index')
    elif request.method == 'GET':

        return render(request, 'Journal/lessons.html', {'titles': sorted_titles,
                                                        'lessons': alllessons, 'lessonsforms': lessonsforms})
    else:
        form = LessonAddForms(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']

            new_lesson = Lesson(title=title)
            new_lesson.save()

            success = True
            return render(request, 'Journal/lessons.html', {'titles': sorted_titles,
                                                            'lessons': alllessons, 'lessonsforms': lessonsforms,
                                                            'success': success})

        error = True
        return render(request, 'Journal/lessons.html', {'titles': sorted_titles,
                                                        'lessons': alllessons, 'lessonsforms': lessonsforms,
                                                        'error': error})


@login_required(login_url='/login/')
def homework(request):
    forms = HomeWorkForms()
    # Admin
    if request.user.groups.get().name == 'Admin':
        homeworks = HomeWork.objects.all()
        submitted_homeworks = ''

    elif request.user.groups.get().name == 'Student':
        student_schedules = Schedule.objects.filter(schoolclass=request.user.schoolclass_set.first()).all()
        homeworks = [s.homework_set.first() for s in student_schedules if s.homework_set.first() is not None]

        submitted_homeworks = [h.homework for h in request.user.submithomework_set.all()]
    else:
        teacher = Teacher.objects.filter(user=request.user).first()
        forms.fields['schedule'].queryset = Schedule.objects.filter(homework=None).filter(lessonteacher=teacher)

        homeworks = teacher.homework_set.all()

        submitted_homeworks = ''

    if request.method == 'GET':
        return render(request, 'Journal/homework.html', {'forms': forms, 'homeworks': homeworks,
                                                         'submitted_homeworks': submitted_homeworks,
                                                         })
    else:
        forms_post = HomeWorkForms(request.POST)
        if forms_post.is_valid():
            thisschedule = forms_post.cleaned_data['schedule']
            text = forms_post.cleaned_data['text']

            iswithfile = forms_post.cleaned_data['isWithFile']

            teacher = Teacher.objects.filter(user=request.user).first()

            new_homework = HomeWork(schedule=thisschedule, text=text, teacher=teacher, isWithFile=iswithfile)
            new_homework.save()

            success = True
            return render(request, 'Journal/homework.html',
                          {'forms': forms, 'success': success, 'homeworks': homeworks})
        else:
            error = True
            return render(request, 'Journal/homework.html', {'forms': forms, 'error': error, 'homeworks': homeworks})


@login_required(login_url='/login/')
def submit_homework(request, homework_id):
    if request.method == 'POST':
        homework_file = request.FILES['homework_file']  # Uploaded file instance
        for_homework = HomeWork.objects.filter(id=homework_id).first()

        submithomework = SubmitHomework(homework=for_homework, file=homework_file, student=request.user)
        submithomework.save()

        return redirect('homework')


@login_required(login_url='/login/')
def submit_individualhomework(request, individualhomework_id):
    if request.method == 'POST':
        homework_file = request.FILES['homework_file']
        individualhomework = IndividualHomework.objects.filter(id=individualhomework_id).first()

        individualhomework.file = homework_file
        individualhomework.save()

        return redirect('individual_homework', request.user.schoolclass_set.first().id, request.user.id)


@login_required(login_url='/login/')
def check_homework(request, homework_id):
    if request.method == 'GET':
        thishomework = HomeWork.objects.filter(id=homework_id).first()
        allgrades = Grade.objects.all()

        return render(request, 'Journal/check_homework.html', {'thishomework': thishomework, 'grades': allgrades})


@login_required(login_url='/login/')
def assign_grade(request, ih_id, submithomework_id, homework_id, schoolclass_id, student_id):
    if request.method == 'POST':
        if ih_id == 0:
            h = SubmitHomework.objects.filter(id=submithomework_id).first()
        else:
            h = IndividualHomework.objects.filter(id=ih_id).first()

        grade = Grade.objects.filter(id=request.POST.get('choosegrade')).first()
        comment = request.POST.get('comment')

        h.grade = grade
        h.comment = comment
        h.save()

        if ih_id == 0:
            return redirect('check_homework', homework_id)
        else:
            return redirect('individual_homework', schoolclass_id, student_id)


@login_required(login_url='/login/')
def download(request, filepath, filename):
    with open(filepath, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = "inline; filename=" + filename
        return response


@login_required(login_url='/login/')
def grades(request):
    if request.method == 'GET':
        gradesforms = GradesForms()

        allgrades = Grade.objects.all()
        return render(request, 'Journal/grades.html', {'gradesforms': gradesforms, 'grades': allgrades})

    else:
        gradesforms = GradesForms(request.POST)

        if gradesforms.is_valid():
            grade = gradesforms.cleaned_data['grade']
            color = gradesforms.cleaned_data['color']

            new_grade = Grade(grade=grade, color=color)
            new_grade.save()

            return redirect('grades')


@login_required(login_url='/login/')
def individual_homework(request, schoolclass_id, student_id):
    student = User.objects.filter(id=student_id).first()

    if request.method == 'GET':
        allgrades = Grade.objects.all()

        if request.user.groups.get().name == 'Student':
            myihomeworks = IndividualHomework.objects.filter(student=request.user).all()
        elif request.user.groups.get().name == 'Teacher':
            myihomeworks = IndividualHomework.objects.filter(teacher=request.user.teacher).all()
        else:
            myihomeworks = IndividualHomework.objects.all()

        forms = IndividualHomeWorkForms()

        schoolclasses = SchoolClass.objects.all()
        schoolclass = SchoolClass.objects.filter(id=schoolclass_id).first()

        students = User.objects.filter(schoolclass=schoolclass).all()

        return render(request, 'Journal/individual_homework.html', {'schoolclasses': schoolclasses,
                                                                    'schoolclass': schoolclass,
                                                                    'students': students, 'student': student,
                                                                    'forms': forms, 'myihomeworks': myihomeworks,
                                                                    'schoolclass_id': schoolclass_id,
                                                                    'student_id': student_id, 'grades': allgrades})

    else:
        forms = IndividualHomeWorkForms(request.POST)
        if forms.is_valid():
            text = forms.cleaned_data['text']
            iswithfile = forms.cleaned_data['isWithFile']
            teacher = Teacher.objects.filter(user=request.user).first()

            new_individualhomework = IndividualHomework(student=student, text=text, teacher=teacher,
                                                        isWithFile=iswithfile)
            new_individualhomework.save()

            return redirect('individual_homework', schoolclass_id, student_id)


@login_required(login_url='/login/')
def close_homework(request, h_id):
    h = HomeWork.objects.filter(id=h_id).first()
    h.delete()
    return redirect('homework')


@login_required(login_url='/login/')
def close_individualhomework(request, h_id):
    h = IndividualHomework.objects.filter(id=h_id).first()
    h.delete()
    return redirect('individual_homework', '0', 0)


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

        # teacher_form = TeacherForm()

        return render(request, 'Journal/profile.html', {'profile_photo': profile_photo, 'curr_user': curr_user,
                                                        'image_form': image_form, 'user_form': user_form,
                                                        })

    else:  # POST
        user_form = UserEditForms(request.POST)
        image_form = UserImageForm(request.POST, request.FILES)
        # teacher_form = TeacherForm(request.POST)
        if image_form.is_valid() and user_form.is_valid():  # and teacher_form.is_valid():
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

            if image is not None:

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

    if user_image is not None:
        user_image.image.delete()
        user_image.delete()

    u.delete()

    return redirect('users')


def logout_view(request):
    logout(request)
    return redirect('index')
