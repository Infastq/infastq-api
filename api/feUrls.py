from django.urls import path
from . import feViews

urlpatterns = [
  path('index', feViews.index),
]