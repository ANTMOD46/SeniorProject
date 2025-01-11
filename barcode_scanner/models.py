# barcode_scanner/models.py
from django.db import models

class WasteImage(models.Model):
    waste_type = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='ประเภทขยะ'
    )
    subtype = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='หมวดหมู่ย่อย'
    )
    category = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='หมวดหมู่'
    )
    separation_method = models.TextField(
        blank=True,
        null=True,
        verbose_name='วิธีการแยกขยะ'
    )



class WasteItem(models.Model):
    WASTE_TYPE_CHOICES = [
        ('plastic', 'พลาสติก'),
        ('paper', 'กระดาษ'),
        ('metal', 'โลหะ'),
        ('glass', 'แก้ว'),
        ('e_waste', 'e-waste'),
        ('steel', 'เหล็ก'),
        ('others', 'อื่นๆ'),
    ]

    CATEGORY_CHOICES = [
        ('recyclable', 'สามารถรีไซเคิลได้'),
        ('non_recyclable', 'ไม่สามารถรีไซเคิลได้'),
        ('hazardous', 'ของเสียอันตราย'),
        ('compostable', 'สามารถย่อยสลายได้'),
    ]

    barcode = models.CharField(max_length=100, unique=True, verbose_name='เลขบาร์โค้ด')
    brand_name = models.CharField(max_length=255, verbose_name='ชื่อยี่ห้อ', default='Unknown')
    product_name = models.CharField(max_length=255, verbose_name='ชื่อสินค้า / รุ่น / ประเภท')
    waste_type = models.CharField(
        max_length=50,
        choices=WASTE_TYPE_CHOICES,
        verbose_name='ประเภทขยะหลัก',
        blank=True,
        null=True
    )
    subtype = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='หมวดหมู่ย่อยของขยะ'
    )
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        verbose_name='หมวดหมู่ของขยะ',
        blank=True,
        null=True
    )
    separation_method = models.TextField(blank=True, null=True, verbose_name='วิธีการแยกขยะ')
    product_image = models.ImageField(upload_to='product_images/', blank=True, null=True, verbose_name='ภาพผลิตภัณฑ์')
    images = models.ManyToManyField('WasteImage', blank=True, verbose_name='รูปภาพที่เกี่ยวข้อง')

    def __str__(self):
        return f"{self.product_name} ({self.barcode})"
