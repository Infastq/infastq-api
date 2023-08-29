from django.db import models

# Create your models here.
class Uang(models.Model):
    Date = models.DateTimeField(auto_now_add=True)
    red_freq = models.IntegerField()
    green_freq = models.IntegerField()
    blue_freq = models.IntegerField()
    value = models.CharField(max_length=20)