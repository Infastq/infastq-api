from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.say_hello),
    path('calculate/', views.calculate),
    path('summary/', views.get_total_uang),
    path('reset/', views.clear, name="reset")
]