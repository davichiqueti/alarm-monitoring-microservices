from rest_framework import viewsets
from core import serialiezers,  models


class AlarmViewSet(viewsets.ModelViewSet):
    queryset = models.Alarm.objects.all()
    serializer_class = serialiezers.AlarmSerializer


class AlarmUserViewSet(viewsets.ModelViewSet):
    queryset = models.AlarmUser.objects.all()
    serializer_class = serialiezers.AlarmUserSerializer
