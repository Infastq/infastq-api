from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from . import serializers, ml_model, models
import json
from rest_framework.decorators import api_view


# Create your views here.
@api_view(['GET'])
def say_hello(request):
    return HttpResponse('Hello World')

@api_view(['POST'])
def calculate(request):
    try:
        request_data = json.loads(request.body.decode('utf-8'))
        value = calculate(request_data['red'], request_data['green'], request_data['blue'])

        # Create a new record in the Uang model
        new_uang_record = models.Uang.objects.create(
            Date=datetime.now(),
            red_freq=request_data['red'],
            green_freq=request_data['green'],
            blue_freq=request_data['blue'],
            value=value
        )

        # Serialize the new Uang record
        serialized_uang = serializers.UangSerializer(new_uang_record).data

        jsonResp = {
            'data': value,
            'status': 'success',
            'uang_record': serialized_uang
        }

    except Exception as e:
        jsonResp = {
            'status':'error',
            'message':str(e),
            'uang_record': None
        }
    return JsonResponse(jsonResp)

@api_view(['GET'])
def get_total_uang(request):
    total_uang = models.Uang.objects.aggregate(models.Sum('value'))['total']
    jsonResp = {
        'total_uang': total_uang,
    }
    return JsonResponse(jsonResp)
