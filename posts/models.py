from django.db import models
from django.conf import settings
from .models import *




from django.db import models
from django.conf import settings

class SellItem(models.Model):
    POST_TYPE_CHOICES = [
        ('sell', 'ประกาศขาย'),
        ('buy', 'ประกาศซื้อ'),
    ]

    post_type = models.CharField(
        max_length=10,
        choices=POST_TYPE_CHOICES,
        default='sell',
        verbose_name='ประเภทประกาศ'
    )
    title = models.CharField(max_length=255, verbose_name='หัวข้อประกาศ')
    description = models.TextField(verbose_name='รายละเอียดสินค้า')
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='ราคา (เฉพาะประกาศขาย)'
    )
    location = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=15, verbose_name='เบอร์โทรติดต่อ')
    image = models.ImageField(upload_to='sell_items/', verbose_name='รูปภาพสินค้า')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='วันที่ประกาศ')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='วันที่แก้ไขประกาศ')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='ผู้ประกาศ'
    )
    is_closed = models.BooleanField(default=False, verbose_name='ปิดการขายแล้วหรือยัง')

    # ฟิลด์ที่เชื่อมโยงกับขยะ
    related_waste = models.ManyToManyField(
        'barcode_scanner.WasteImage',  # ระบุเส้นทางเต็มของโมเดล
        blank=True,
        related_name='sell_items',
        verbose_name="ขยะที่เกี่ยวข้อง"
    )

    def __str__(self):
        return self.title




    
class SellItemComment(models.Model):
    sell_item = models.ForeignKey(SellItem, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    


class Donation(models.Model):
    ROLE_CHOICES = [
        ('donor', 'ผู้บริจาค'),
        ('recipient', 'ผู้รับบริจาค'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='donor')  # ประเภทผู้บริจาค
    title = models.CharField(max_length=255)  # ชื่อการบริจาค
    description = models.TextField()  # รายละเอียดของการบริจาค
    location = models.CharField(max_length=255)  # สถานที่
    phone = models.CharField(max_length=15)  # เบอร์โทรศัพท์
    image = models.ImageField(upload_to='donations/')  # รูปภาพการบริจาค
    created_at = models.DateTimeField(auto_now_add=True)  # วันที่สร้างการบริจาค
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # ผู้ใช้ที่ทำการบริจาค
    is_closed = models.BooleanField(default=False)  # สถานะการปิดการบริจาค

    def __str__(self):
        return self.title
    


class DonationComment(models.Model):
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class GeneralAnnouncement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    location = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='announcements/', blank=True, null=True)  # เพิ่มฟิลด์นี้
    

    def __str__(self):
        return self.title


class GeneralAnnouncementComment(models.Model):
    general_announcement = models.ForeignKey(GeneralAnnouncement, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)