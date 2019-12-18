from django import forms


class AuthForms(forms.Form):
    username = forms.CharField(label='Username:', max_length=100)
    password = forms.CharField(label='Password:', max_length=200)


class ClassEditForms(forms.Form):
    title = forms.CharField(max_length=3)
