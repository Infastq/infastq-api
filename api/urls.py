from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.say_hello),
    path('calculate/', views.calculate),
    path('summary/', views.get_total_uang),
    path('reset/', views.clear, name="reset"),
    path('convert_to_rgb/', views.convert_image_to_r5g6b5, name="convert_to_rgb")
]