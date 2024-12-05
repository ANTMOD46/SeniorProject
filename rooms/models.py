from django.db import models
from django.conf import settings  # ใช้ settings.AUTH_USER_MODEL แทน User model เพื่อให้ยืดหยุ่น

class Room(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    

    def __str__(self):
        return self.name

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')  # เชื่อมโยงกับ Room
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # ใช้ CustomUser ผ่าน AUTH_USER_MODEL
    content = models.TextField()  # เนื้อหาข้อความ
    timestamp = models.DateTimeField(auto_now_add=True)  # เวลาที่ส่งข้อความ

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}: {self.content}"

