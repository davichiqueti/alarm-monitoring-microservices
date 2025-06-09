from core import models
from rest_framework import serializers


class AlarmUserSerializer(serializers.ModelSerializer):
    class Meta():
        model = models.AlarmUser
        exclude = ['pk']


class MonitoringSpotSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MonitoringSpot
        fields = ['name']


class AlarmSerializer(serializers.ModelSerializer):
    alarm_users = AlarmUserSerializer(many=True, read_only=True)
    monitoring_spots = MonitoringSpotSerializer(many=True, required=False)

    class Meta():
        model = models.Alarm
        fields = '__all__'

    def create(self, validated_data):
        spots_data = validated_data.pop('monitoring_spots', [])
        alarm = super().create(validated_data)
        for spot in spots_data:
            models.MonitoringSpot.objects.create(alarm=alarm, **spot)
        return alarm

    def update(self, instance, validated_data):
        spots_data = validated_data.pop('monitoring_spots', None)
        alarm = super().update(instance, validated_data)
        if spots_data is not None:
            instance.monitoring_spots.all().delete()
            for spot in spots_data:
                models.MonitoringSpot.objects.create(alarm=alarm, **spot)
        return alarm
