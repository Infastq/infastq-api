from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from . import serializers, ml_model, models, utils
import json
import base64
import os
import requests
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, viewsets
import numpy as np
import traceback
from django.conf import settings

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

@api_view(['POST'])
def convert_image_to_r5g6b5(request, id1, id2):
    if request.method == 'POST':
        try:
            if json.loads(request.body.decode('utf-8')).get('python') == 1:
                img_link = os.path.join(settings.MEDIA_ROOT, 'uploads/images/qr', 'python.jpg')
                with open(img_link, 'rb') as image_file:
                    image_data = image_file.read()
            else:
                image_file = request.data.get('image')  # Assuming your file input is named 'image'
                if image_file:
                    image_data = image_file.read()
                else:
                    return JsonResponse({"error": "No image file provided"}, status=400)
            if image_file:
                # Read the uploaded image data

                # Convert image data to 16-bit RGB array
                array = utils.convert_to_r5g6b5(image_data)

                if id1 < 0:
                    id1 = 0
                if id2 > len(array):
                    id2 = len(array)


                # Optionally, encode the array as base64 if needed
                # base64_image_data = base64.b64encode(array.tobytes()).decode('utf-8')
                subarray = array[id1:id2]
                return JsonResponse({
                    "data": subarray,
                    "message": "Image uploaded successfully"
                })
            else:
                return JsonResponse({"error": "No image file provided"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error processing image: {str(e)}\n{traceback.format_exc()}"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
    
latitude = -6.878934
longitude = 107.612385
  
@api_view(['POST', 'GET'])
def gps_data(request):
    global latitude, longitude
    if request.method == 'POST':
        try:
            request_data = json.loads(request.body.decode('utf-8'))
            jsonResp = {
                "latitude": request_data["latitude"],
                "longitude": request_data["longitude"]
            }
            latitude = request_data['latitude']
            longitude = request_data["longitude"]
            return JsonResponse(jsonResp, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    elif request.method == 'GET':
        try:
            if latitude is not None and longitude is not None:
                json_resp = {
                    "latitude": latitude,
                    "longitude": longitude
                }
                return Response(json_resp, status=status.HTTP_200_OK)
            else:
                return Response({"error": "GPS data not available"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

# for demo purpose
lat_masjid = -6.922241
lon_masjid = 107.607020

@api_view(['GET'])
def check_out_of_range(request):
    global latitude, longitude, lat_masjid, lon_masjid
    distance = 0
    try:
        distance = utils.distance(latitude, longitude, lat_masjid, lon_masjid)
    except Exception as e:
        return JsonResponse({"error" : f"calculation error : {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    
    # threshold 2 km
    if distance > 2:
        return JsonResponse({"out_of_range": True, "warning": "Kotak amal di luar jangkauan", "distance" : distance}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"out_of_range": False, "distance": distance}, status=status.HTTP_200_OK)
    
@api_view(['GET','POST'])
def location_masjid(request):
    if request.method == 'POST':
        try:
            request_data = json.loads(request.body.decode('utf-8'))
            serializer = serializers.MasjidSerializer(data=request_data)

            if serializer.is_valid():
                new_masjid_record = serializer.save()
                serialized_masjid = serializers.MasjidSerializer(new_masjid_record).data
                serialized_masjid = json.dumps(serialized_masjid, indent=3)
                serialized_masjid['luas'] = float(serialized_masjid['luas'])
                serialized_masjid['latitude'] = float(serialized_masjid['latitude'])
                serialized_masjid['longitude'] = float(serialized_masjid['longitude'])

                jsonResp = {
                    "status": "success",
                    "message": "New Data Created",
                    "data": serialized_masjid
                }
                return JsonResponse(jsonResp, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse(
                    {
                        "status": "error",
                        "error": serializer.errors,
                        "data": None
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return JsonResponse(
                {
                    "status": "error",
                    "error": str(e),
                    "data": None
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    elif request.method == 'GET':
        try:
            data_masjid = models.Masjid.objects.all()
            serialized_masjid = serializers.MasjidSerializer(data_masjid, many=True).data
            serialized_masjid = json.dumps(serialized_masjid, indent=3)
            serialized_masjid['luas'] = float(serialized_masjid['luas'])
            serialized_masjid['latitude'] = float(serialized_masjid['latitude'])
            serialized_masjid['longitude'] = float(serialized_masjid['longitude'])


            jsonResp = {
                "status": "success",
                "message": "Data Masjid Diambil",
                "data": serialized_masjid
            }
            return JsonResponse(jsonResp, status=status.HTTP_200_OK)
        except Exception as e:
            jsonResp = {
                "status": "error",
                "message": str(e),
                "data": None
            }
            return JsonResponse(jsonResp, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'PUT'])
def location_masjid_by_id(request, id):
    if request.method == 'GET':
        try:
            data_masjid = models.Masjid.objects.get(id=id)
            serialized_masjid = serializers.MasjidSerializer(data_masjid).data
            serialized_masjid = json.dumps(serialized_masjid, indent=3)
            serialized_masjid['luas'] = float(serialized_masjid['luas'])
            serialized_masjid['latitude'] = float(serialized_masjid['latitude'])
            serialized_masjid['longitude'] = float(serialized_masjid['longitude'])

            jsonResp = {
                "status": "success",
                "message": "Data Masjid Diambil",
                "data": serialized_masjid
            }
            return JsonResponse(jsonResp, status=status.HTTP_200_OK)
        except models.Masjid.DoesNotExist:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Data Masjid dengan ID yang diberikan tidak ditemukan",
                    "data": None
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            jsonResp = {
                "status": "error",
                "message": str(e),
                "data": None
            }
            return JsonResponse(jsonResp, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == 'PUT':
        try:
            data_masjid = models.Masjid.objects.get(id=id)
            request_data = json.loads(request.body.decode('utf-8'))

            # Update the Masjid object with the new data
            data_masjid.nama = request_data.get("nama", data_masjid.nama)
            data_masjid.alamat = request_data.get("alamat", data_masjid.alamat)
            data_masjid['luas'] = request_data.get("luas", data_masjid['luas'])
            data_masjid['latitude'] = request_data.get("latitude", data_masjid['latitude'])
            data_masjid['longitude'] = request_data.get("longitude", data_masjid['longitude'])

            # Save the updated object
            data_masjid.save()

            serialized_masjid = serializers.MasjidSerializer(data_masjid).data
            serialized_masjid = json.dumps(serialized_masjid, indent=3)
            serialized_masjid['luas'] = float(serialized_masjid['luas'])
            serialized_masjid['latitude'] = float(serialized_masjid['latitude'])
            serialized_masjid['longitude'] = float(serialized_masjid['longitude'])

            jsonResp = {
                "status": "success",
                "message": "Data Masjid Updated",
                "data": serialized_masjid
            }
            return JsonResponse(jsonResp, status=status.HTTP_200_OK)
        except models.Masjid.DoesNotExist:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Data Masjid dengan ID yang diberikan tidak ditemukan",
                    "data": None
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            jsonResp = {
                "status": "error",
                "message": str(e),
                "data": None
            }
            return JsonResponse(jsonResp, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def index(request):
    return render(request, 'index.html')

