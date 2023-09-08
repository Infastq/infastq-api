from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.say_hello),
    path('calculate/', views.calculate),
    path('summary/', views.get_total_uang),
    path('reset/', views.clear, name="reset"),
    path('convert_to_rgb/<int:id1>-<int:id2>', views.convert_image_to_r5g6b5, name="convert_to_rgb"),
    path('location/', views.gps_data, name="location"),
    path('check_range/', views.check_out_of_range, name="check_range"),
    path('masjid/', views.location_masjid, name='masjid'),
    path('masjid/<int:id>', views.location_masjid_by_id, name="masjid_by_id")
]