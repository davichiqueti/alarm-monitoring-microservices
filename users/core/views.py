from core import serialiezers, models
from rest_framework import viewsets


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serialiezers.UserSerializer
