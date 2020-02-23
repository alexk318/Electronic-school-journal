from django import forms
from .models import Day, Lesson, SchoolClass, Schedule

days = Day.objects.all()
days_choices = [tuple([d, d]) for d in days]

lessons = Lesson.objects.all()
lessons_choices = [tuple([l, l]) for l in lessons]


class AuthForms(forms.Form):
    username = forms.CharField(label='Username:', max_length=100, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password:', max_length=200, required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class ClassAddForms(forms.ModelForm):
    class Meta:
        model = SchoolClass
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'})
        }


class ScheduleAddForms(forms.Form):
    day_week = forms.CharField(label='Day of the week:', widget=forms.Select(choices=days_choices))
    lesson = forms.CharField(label='Lesson:', widget=forms.Select(choices=lessons_choices, attrs={'format': '%Y-%m-%d'})
                             )

    lesson_date = forms.DateField(label='Lesson date:', widget=forms.SelectDateWidget)

    lesson_start = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    lesson_end = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
