from django.db import models
from django.contrib.auth.models import User

from datetime import datetime


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

    date = models.CharField(max_length=20, default='')

    start = models.CharField(max_length=20, default='')
    end = models.CharField(max_length=20, default='')

    def __str__(self):
        return 'Class: {}, Date: {}, Lesson: {}'.format(self.schoolclass, self.date, self.lesson)
