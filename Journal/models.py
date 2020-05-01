from django.db import models
from django.contrib.auth.models import User

import os


class Grade(models.Model):
    grade = models.CharField(max_length=3)
    color = models.CharField(max_length=7, null=True)


class UserImage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', null=True, blank=True)


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)


class SchoolClass(models.Model):
    title = models.CharField(max_length=3, default="", unique=True)
    students = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return '%s' % self.title.capitalize()


class Lesson(models.Model):
    title = models.CharField(max_length=50, default="", unique=True)

    def __str__(self):
        return '%s' % self.title


class Day(models.Model):
    title = models.CharField(max_length=10, default="", unique=True)

    def __str__(self):
        return '%s' % self.title


class Schedule(models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE, default="")
    schoolclass = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, default="")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, default="")

    lessonteacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, default="", blank=True, null=True)

    date = models.DateField(blank=True, null=True)

    start = models.TimeField(blank=True, null=True)
    end = models.TimeField(blank=True, null=True)

    def __str__(self):
        return 'Schoolclass: {}, Lesson: {}'.format(self.schoolclass, self.lesson)


class HomeWork(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, default="", null=True)

    text = models.TextField(default="")

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, default="")

    isWithFile = models.BooleanField(default=False)

    def get_teacher(self):
        return self.schedule.lessonteacher


class SubmitHomework(models.Model):
    homework = models.ForeignKey(HomeWork, on_delete=models.CASCADE)
    file = models.FileField(upload_to='files/', null=True, blank=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, default="")

    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, default="", null=True)
    comment = models.TextField(default="", null=True)

    def get_filename(self):
        path = self.file.path
        base = os.path.basename(path)

        return base


class IndividualHomework(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, default="", null=True)
    text = models.TextField(default="", null=True)

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, default="")

    isWithFile = models.BooleanField(default=False)
    file = models.FileField(upload_to='files/', null=True, blank=True)

    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, default="", null=True)
    comment = models.TextField(default="", null=False)

    def get_filename(self):
        path = self.file.path
        base = os.path.basename(path)

        return base
