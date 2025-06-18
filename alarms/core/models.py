from django.db import models, IntegrityError
import requests
import os


class Alarm(models.Model):
    active = models.BooleanField(default=False)
    title = models.TextField(max_length=60)
    description = models.TextField(max_length=120, null=True, blank=True)
    location = models.TextField(max_length=60, null=False, blank=False)


class MonitoringSpot(models.Model):
    alarm = models.ForeignKey(Alarm, on_delete=models.CASCADE, related_name="monitoring_spots")
    name = models.CharField(max_length=60)


class AlarmUser(models.Model):
    class PermissionLevel(models.TextChoices):
        VIEWER = (
            'viewer',
            'Can view alarm information and activity, but cannot make changes.'
        )
        EDITOR = (
            'editor',
            'Can edit information from the alarm'
        )
        OWNER = (
            'owner',
            'Full control over the alarm. Including adding member and delete the alarm'
        )

    pk = models.CompositePrimaryKey("alarm", "user")
    alarm = models.ForeignKey(Alarm, on_delete=models.CASCADE, related_name="alarm_users")
    user = models.PositiveIntegerField()
    notify = models.BooleanField(default=True)
    permission = models.CharField(
        max_length=10,
        choices=PermissionLevel.choices,
        default=PermissionLevel.VIEWER
    )
