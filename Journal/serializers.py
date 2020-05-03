from rest_framework import serializers
from .models import User

# Serializers (Сериализаторы) позволяют преобразовывать сложные данные, такие как наборы запросов querysets и
# объекты моделей, в типы данных Python, которые затем можно легко преобразовать в JSON, XML или другие content types.


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
        return User.objects.create(**validated_data)