from django import forms


class AuthForms(forms.Form):
    username = forms.CharField(label='Username:', max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password:', max_length=200, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))


class ClassAddForms(forms.Form):
    title = forms.CharField(label='Title:', max_length=3)

