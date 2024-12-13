from django.db import models
from django.conf import settings
from .models import *




class SellItem(models.Model):
    user_role = models.CharField(max_length=20, choices=[
        ('buyer', 'ผู้ซื้อ'),
        ('seller', 'ผู้ขาย'),
    ], default='buyer')
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)  # ฟิลด์โลเคชั่น
    phone = models.CharField(max_length=15)  # ฟิลด์เบอร์โทรศัพท์
    image = models.ImageField(upload_to='sell_items/')
    created_at = models.DateTimeField(auto_now_add=True)  # เพิ่มวันที่ประกาศ
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_closed = models.BooleanField(default=False)  # ฟิลด์เพื่อบันทึกว่าสินค้าปิดการขายแล้วหรือยัง
    

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