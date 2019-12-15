from django.db import models


class Class(models.Model):
    title = models.CharField(max_length=3, default="", editable=False)

    def __str__(self):
        return '%s' % self.title.capitalize()
