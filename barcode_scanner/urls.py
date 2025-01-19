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
    path('add-waste-detail/<str:barcode>/', views.add_waste_detail, name='add_waste_detail'),
    
    path('vote-correct/<int:image_id>/', views.vote_correct, name='vote_correct'),
    path('vote-incorrect/<int:image_id>/', views.vote_incorrect, name='vote_incorrect'),
    path('update-votes/<int:image_id>/', views.update_votes, name='update_votes'),
    path('delete/<int:pk>/', views.delete_waste_item, name='delete_waste_item'),
 
    path('all-barcodes/', views.all_barcodes, name='all_barcodes'),
    path('my-waste-details/', views.my_waste_details, name='my_waste_details'),
    
    
   
      
    
    # ใหม่
    
    
]

