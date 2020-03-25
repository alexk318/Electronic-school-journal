from django.db import models
from django.contrib.auth.models import User


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
        return 'Day: {}, Lesson: {}'.format(self.day, self.lesson)


class HomeWork(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, default="")
    text = models.TextField(default="")

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, default="")

    def get_teacher(self):
        return self.schedule.lessonteacher
