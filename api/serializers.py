from rest_framework import serializers
from .models import *

class UangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uang
        fields = '__all__'

class WifiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wifi
        fields = '__all__'