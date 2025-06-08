from rest_framework import viewsets, generics
from core import serialiezers, models
import requests
import os


class AlarmViewSet(viewsets.ModelViewSet):
    queryset = models.Alarm.objects.all()
    serializer_class = serialiezers.AlarmSerializer

    def perform_update(self, serializer):
        old_obj = self.get_object()
        updated_obj = serializer.save()
        if old_obj.active != updated_obj.active:
            notification_type = "activated" if updated_obj.active else "deactivated"
            requests.post(
                url=f"{os.environ['NOTIFICATION_SERVICE_URL']}/notify/",
                json={
                    "alarm": updated_obj.id,
                    "notification_type": notification_type
                }
            )

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
