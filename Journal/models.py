from django.db import models
from django.contrib.auth.models import User


class SchoolClass(models.Model):
    title = models.CharField(max_length=3, default="", editable=False, unique=True)
    students = models.ManyToManyField(User)

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

    def __str__(self):
        return 'Class: {}, Lesson: {}'.format(self.schoolclass, self.lesson)
