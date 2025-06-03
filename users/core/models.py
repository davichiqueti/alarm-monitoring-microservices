from django.db import models


class User(models.Model):
    username = models.CharField(max_length=60, unique=True, blank=False)
    name = models.CharField(max_length=90, blank=False)
    email = models.CharField(max_length=90, unique=True, blank=False)
    cellphone = models.CharField(max_length=30, unique=True, blank=False)
