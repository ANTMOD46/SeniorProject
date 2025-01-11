from django.urls import path
from . import views

app_name = 'barcode_scanner'
urlpatterns = [
    path('scan/', views.scan_barcode_redirect, name='scan_barcode_redirect'),
    path('scan-camera/', views.scan_camera, name='scan_camera'),
    path('scan-result/', views.scan_result, name='scan_result'),
    path('submit-form/', views.submit_form, name='submit_form'),
    path('form/', views.form_view, name='form_view'),
    path('success/', views.success, name='success'),
    # path('add/', views.add_waste_item, name='add_waste_item'),
    path('search/', views.search_waste_item, name='search_waste_item'),
    # path('<int:pk>/', views.waste_item_detail, name='waste_item_detail'),
    path('detail/<int:pk>/', views.waste_item_detail, name='waste_item_detail'),
    # เพิ่ม URL pattern สำหรับ waste_item_detail
    path('add/', views.add_waste_item, name='add_waste_item'),
    
]

