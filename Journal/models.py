from django.db import models
from django.contrib.auth.models import User


class SchoolClass(models.Model):
    title = models.CharField(max_length=3, default="", editable=False, unique=True)
    student = models.ForeignKey(User, default="", on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % self.title.capitalize()
