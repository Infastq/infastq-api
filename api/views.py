from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from . import serializers, ml_model, models, utils
import json
import base64
import os
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, viewsets
import numpy as np

class UploadImageViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = serializers.UploadedImageSerializer(data=request.data)

        if serializer.is_valid():
            # Delete the previous image (if it exists)
            try:
                old_image = serializers.UploadedImage.objects.first()
                os.remove(old_image.image.path)
                old_image.delete()
            except serializers.UploadedImage.DoesNotExist:
                pass

            # Save the new image
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
@api_view(['GET'])
def say_hello(request):
    return HttpResponse('Hello World')

@api_view(['POST'])
def calculate(request):
    try:
        request_data = json.loads(request.body.decode('utf-8'))
        value = ml_model.calculate(request_data['red'], request_data['green'], request_data['blue'])

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
    total_uang = models.Uang.objects.aggregate(models.Sum('value'))['value__sum']
    if total_uang is None:
        total_uang = 0
    jsonResp = {
        'total_uang': total_uang,
    }
    return JsonResponse(jsonResp)

@api_view(['DELETE'])
def clear(request):
    try:
        # Delete all records from the Uang model
        models.Uang.objects.all().delete()

        jsonResp = {
            'status': 'success',
            'message': 'All records deleted',
        }
    except Exception as e:
        jsonResp = {
            'status': 'error',
            'message': str(e),
        }
    return JsonResponse(jsonResp)

def convert_image_to_r5g6b5(request):
    if request.method == 'POST':
        try:
            image_file = request.FILES['image']  # Assuming your file input is named 'image'
            if image_file:
                # Read the uploaded image data
                image_data = image_file.read()

                # Convert image data to 16-bit RGB array
                array = utils.convert_to_r5g6b5(image_data)

                # Optionally, encode the array as base64 if needed
                # base64_image_data = base64.b64encode(array.tobytes()).decode('utf-8')

                return JsonResponse({
                    "data": array,
                    "message": "Image uploaded successfully"
                })
            else:
                return JsonResponse({"error": "No image file provided"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error processing image: {str(e)}"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

def index(request):
    return render(request, 'index.html')
