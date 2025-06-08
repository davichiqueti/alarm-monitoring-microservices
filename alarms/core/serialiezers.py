from core import models
from rest_framework import serializers


class AlarmUserSerializer(serializers.ModelSerializer):
    class Meta():
        model = models.AlarmUser
        exclude = ['pk']


class AlarmSerializer(serializers.ModelSerializer):
    alarm_users = AlarmUserSerializer(many=True, read_only=True)

    class Meta():
        model = models.Alarm
        fields = '__all__'
