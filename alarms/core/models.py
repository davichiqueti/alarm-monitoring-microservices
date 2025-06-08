from django.db import models, IntegrityError
import requests


class Alarm(models.Model):
    active = models.BooleanField(default=False)
    title = models.TextField(max_length=60)
    description = models.TextField(max_length=120, null=True, blank=True)


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

    def save(self, **kwargs):
        # TODO: Only check when user attribute changed
        if not self.check_user(self.user):
            raise IntegrityError(f"Could not find valid User with ID {self.user} on User Application.")
        # Continues to normal flow.
        super().save(**kwargs) 

    def check_user(self, user_id: int) -> bool:
        res = requests.get(f"http://users-app:8000/api/users/{user_id}/")
        return res.status_code == 200
