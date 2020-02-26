from django.contrib import admin
from .models import SchoolClass, Lesson, Day, Schedule, HomeWork, UserImage

admin.site.register(UserImage)

admin.site.register(SchoolClass)
admin.site.register(Lesson)
admin.site.register(Day)
admin.site.register(Schedule)
admin.site.register(HomeWork)
