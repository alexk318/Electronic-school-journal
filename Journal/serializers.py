from rest_framework import serializers
from django.contrib.auth.models import User

from Journal.models import Lesson, Schedule, Day, Grade, Teacher, SchoolClass, HomeWork, IndividualHomework


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


class SchoolClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolClass
        fields = '__all__'


class DaySerialiizer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'


class HomeWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeWork
        fields = '__all__'


class IndividualHomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndividualHomework
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email', 'groups')

    def create(self, validated_data):
        groups_data = validated_data.pop('groups')
        user = User.objects.create(**validated_data)

        for group_data in groups_data:
            user.groups.add(group_data)

            if group_data.name == 'Teacher':
                t = Teacher(user=user)
                t.save()

        return user
