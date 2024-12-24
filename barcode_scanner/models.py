from django.db import models

class WasteItem(models.Model):
    barcode = models.CharField(max_length=100, unique=True)  # รหัสบาร์โค้ด
    product_name = models.CharField(max_length=255)  # ชื่อผลิตภัณฑ์
    waste_type = models.CharField(max_length=50)  # ประเภทขยะ (พลาสติก, แก้ว, โลหะ, ฯลฯ)
    subtype = models.CharField(max_length=50, blank=True, null=True)  # ประเภทย่อย เช่น PE, HDPE
    category = models.CharField(max_length=50)  # หมวดหมู่ เช่น รีไซเคิล, อินทรีย์
    waste_image = models.ImageField(upload_to='waste_images/', blank=True, null=True)  # ภาพขยะ
    separation_method = models.TextField(blank=True, null=True)  # วิธีการแยกขยะ

    created_at = models.DateTimeField(auto_now_add=True)  # เวลาที่เพิ่มข้อมูล
    updated_at = models.DateTimeField(auto_now=True)  # เวลาที่แก้ไขข้อมูลล่าสุด

    def __str__(self):
        return f"{self.product_name} ({self.barcode})"
