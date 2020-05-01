from django.contrib.auth.models import Group


def get_data(handler):
    username = handler.cleaned_data['username']
    password = handler.cleaned_data['password']
    first_name = handler.cleaned_data['first_name']
    last_name = handler.cleaned_data['last_name']
    email = handler.cleaned_data['email']

    group = handler.cleaned_data['group']
    groups = Group.objects.get(name=group)

    return {'username': username, 'password': password, 'first_name': first_name, 'last_name': last_name,
            'email': email,
            'group': group, 'groups': groups}
