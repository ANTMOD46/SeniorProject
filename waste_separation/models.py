from django.db import models
import uuid

class WasteItem(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4, editable=False)  # Primary Key
    barcode = models.CharField(max_length=50, unique=True, verbose_name="รหัสบาร์โค้ด")  # รหัสบาร์โค้ด
    name = models.CharField(max_length=255, verbose_name="ชื่อผลิตภัณฑ์")  # ชื่อผลิตภัณฑ์ (เช่น ขวดน้ำดื่ม, กล่องนม)
    waste_type = models.CharField(max_length=100, verbose_name="ประเภทขยะ")  # ประเภทขยะ (พลาสติก, โลหะ, กระดาษ)
    image = models.ImageField(upload_to="waste_images/", verbose_name="รูปภาพผลิตภัณฑ์")  # รูปภาพของผลิตภัณฑ์
    disposal_method = models.TextField(verbose_name="วิธีแยกขยะ")  # วิธีแยกขยะหรือรีไซเคิล
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="วันที่เพิ่มข้อมูล")  # วันที่บันทึกข้อมูล

    def __str__(self):
        return self.name
