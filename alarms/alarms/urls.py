from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from core import views


router = routers.DefaultRouter()
router.register(r'alarms', viewset=views.AlarmViewSet, basename="Alarms")
router.register(r'alarms-users', viewset=views.AlarmUserViewSet, basename="Alarms Users")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls))
]
