from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login

import re

from .forms import AuthForms
from .models import Class


def index(request):
    if request.user.is_authenticated:
        return redirect('journal')
    else:
        if request.method == 'POST':
            forms = AuthForms(request.POST)
            if forms.is_valid():
                username = forms.cleaned_data['username']
                password = forms.cleaned_data['password']

                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('journal')
                else:
                    msg = 'The entered data is incorrect'
                    return render(request, 'Journal/index.html', {'forms': forms, 'msg': msg})

        forms = AuthForms()
        return render(request, 'Journal/index.html', {'forms': forms})


def journal(request):
    if request.user.is_authenticated:
        return render(request, 'Journal/journal.html', {'current_user': request.user,
                                                        'group': request.user.groups.values_list('name', flat=True).
                      first()})
    else:
        msg = 'To access the journal you need to log in!'
        forms = AuthForms()
        return render(request, 'Journal/index.html', {'forms': forms, 'msg': msg})


def schedule(request):
    if request.user.groups.values_list('name', flat=True).first() != 'Admin':
        return redirect('index')
    return render(request, 'Journal/schedule.html', {})


def classes(request):
    if request.user.groups.values_list('name', flat=True).first() != 'Admin':
        return render(request, 'Journal/index.html', {})
    else:
        classes = Class.objects.all()
        titles = [classes_.title for classes_ in classes ]

        def key(s):
            num, letters = re.match(r'(\d*)(.*)', s).groups()
            return float(num or 'inf'), letters

        sorted_titles = sorted(titles, key=key)

        return render(request, 'Journal/classes.html', {'titles': sorted_titles})


def logout_view(request):
    logout(request)
    return redirect('index')
