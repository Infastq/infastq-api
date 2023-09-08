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

class MasjidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Masjid
        fields = '__all__'