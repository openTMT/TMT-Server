from rest_framework import serializers
from .models import *


class iOSDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = iOSDevice
        fields = '__all__'
