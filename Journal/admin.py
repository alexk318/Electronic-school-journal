from django.contrib import admin
from .models import SchoolClass, Lesson, Day, Schedule

admin.site.register(SchoolClass)
admin.site.register(Lesson)
admin.site.register(Day)
admin.site.register(Schedule)
