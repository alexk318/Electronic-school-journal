from rest_framework import serializers
from django.contrib.auth.models import User, Group

# Serializers (Сериализаторы) позволяют преобразовывать сложные данные, такие как наборы запросов querysets и
# объекты моделей, в типы данных Python, которые затем можно легко преобразовать в JSON, XML или другие content types.


student = Group.objects.get(name='Student')


class ScheduleSerializer(serializers.Serializer):
    date = serializers.DateField()
    start = serializers.TimeField()
    end = serializers.TimeField()


class StudentsSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    first_name = serializers.CharField()
    last_name = serializers.CharField()

    email = serializers.EmailField()

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'], password=validated_data['password'],
                                        first_name=validated_data['first_name'], last_name=validated_data['last_name'],
                                        email=validated_data['email'])

        student.user_set.add(user)

        return user
