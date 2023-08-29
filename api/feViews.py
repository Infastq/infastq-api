from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from . import serializers, ml_model, models
import json
import os
from rest_framework.decorators import api_view

def index(request):
    return render(request, 'index.html')