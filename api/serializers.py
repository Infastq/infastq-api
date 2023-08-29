from rest_framework import serializers
from .models import *

class UangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uang
        fields = '__all__'