from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .forms import AuthForms


def index(request):
    if request.method == 'POST':
        forms = AuthForms(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                return HttpResponseRedirect('/journal')
            else:
                msg = 'The entered data is incorrect'
                return render(request, 'Journal/index.html', {'forms': forms, 'msg': msg})

    forms = AuthForms()
    return render(request, 'Journal/index.html', {'forms': forms})


def journal(request):
    return render(request, 'Journal/journal.html')