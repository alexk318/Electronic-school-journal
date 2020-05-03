from rest_framework import serializers

# Serializers (Сериализаторы) позволяют преобразовывать сложные данные, такие как наборы запросов querysets и
# объекты моделей, в типы данных Python, которые затем можно легко преобразовать в JSON, XML или другие content types.


class ScheduleSerializer(serializers.Serializer):
    date = serializers.DateField()
    start = serializers.TimeField()
    end = serializers.TimeField()