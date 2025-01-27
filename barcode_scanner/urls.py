from django.urls import path
from . import views

app_name = 'barcode_scanner'

urlpatterns = [
    # สแกนและการจัดการบาร์โค้ด
    path('scan-camera/', views.scan_camera, name='scan_camera'),
    path('scan-camera-guest/', views.scan_camera_guest, name='scan_camera_guest'),
    path('handle-barcode/', views.handle_barcode_guest, name='handle_barcode_guest'),
    path('scan-member/', views.handle_barcode_member, name='handle_barcode_member'),

    # การเพิ่มและแก้ไขข้อมูล
    path('add/', views.add_waste_item, name='add_waste_item'),
    path('add-waste-detail/<str:barcode>/', views.add_waste_detail, name='add_waste_detail'),
    path('add-item/', views.add_waste_item, name='add_waste_item'),

    # การแสดงรายละเอียด
    path('detail/<int:pk>/', views.waste_item_detail, name='waste_item_detail'),
    path('waste-item/<int:pk>/', views.waste_item_detail, name='waste_item_detail'),

    # โหวตและการจัดการภาพ
    path('vote-correct/<int:image_id>/', views.vote_correct, name='vote_correct'),
    path('vote-incorrect/<int:image_id>/', views.vote_incorrect, name='vote_incorrect'),
    path('update-votes/<int:image_id>/', views.update_votes, name='update_votes'),
    path('delete-waste-image/<int:pk>/', views.delete_waste_image, name='delete_waste_image'),

    # การลบข้อมูล
    path('delete/<int:pk>/', views.delete_waste_item, name='delete_waste_item'),

    # การจัดการข้อมูลบาร์โค้ดทั้งหมด
    path('all-barcodes/', views.all_barcodes, name='all_barcodes'),
    path('my-waste-details/', views.my_waste_details, name='my_waste_details'),

    # ฟอร์มและการส่งข้อมูล
    path('form/', views.form_view, name='form_view'),

]
