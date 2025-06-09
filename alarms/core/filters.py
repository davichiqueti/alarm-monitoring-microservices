import django_filters
from core.models import Alarm


class AlarmFilter(django_filters.FilterSet):
    user = django_filters.NumberFilter(field_name="alarm_users__user")

    class Meta:
        model = Alarm
        fields = "__all__"
