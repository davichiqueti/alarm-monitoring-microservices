from rest_framework import viewsets, generics
from core import serialiezers, models


class AlarmViewSet(viewsets.ModelViewSet):
    queryset = models.Alarm.objects.all()
    serializer_class = serialiezers.AlarmSerializer


class AlarmUserViewSet(viewsets.ModelViewSet):
    queryset = models.AlarmUser.objects.all()
    serializer_class = serialiezers.AlarmUserSerializer

    def get_object(self):
        # Get the 'pk' from URL, which will be in format 'alarm_id-user_id'
        composite_key = self.kwargs.get('pk')
        try:
            alarm_id, user_id = composite_key.split('-')
            return self.queryset.get(alarm=alarm_id, user=user_id)
        except (ValueError, models.AlarmUser.DoesNotExist):
            raise generics.Http404
