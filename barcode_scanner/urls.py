from django.urls import path
from . import views

app_name = 'barcode_scanner'
urlpatterns = [
    path('scan/', views.scan_barcode, name='scan_barcode'),
    path('scan-camera/', views.scan_camera, name='scan_camera'),
    path('scan-result/', views.scan_result, name='scan_result'),
    path('submit-form/', views.submit_form, name='submit_form'),
     
     
]
