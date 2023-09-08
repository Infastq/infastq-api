from django.db import models
from django.db.models import Sum
from decimal import Decimal
import uuid

# Create your models here.
class Uang(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Date = models.DateTimeField(auto_now_add=True)
    red_freq = models.IntegerField()
    green_freq = models.IntegerField()
    blue_freq = models.IntegerField()
    value = models.PositiveIntegerField()

class Wifi(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ssid = models.CharField(max_length=30)
    password = models.CharField(max_length=70)

class Masjid(models.Model):
    nama = models.CharField(max_length=30)
    alamat = models.CharField(max_length=100)
    luas = models.DecimalField(max_digits=16, decimal_places=2)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
