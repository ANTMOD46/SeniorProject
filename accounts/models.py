from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings  # ใช้ settings.AUTH_USER_MODEL

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=100, verbose_name='ชื่อ')
    last_name = models.CharField(max_length=100, verbose_name='นามสกุล')
    address = models.TextField(verbose_name='ที่อยู่', blank=True, null=True)
    phone_number = models.CharField(max_length=15, verbose_name='เบอร์โทรศัพท์', blank=True, null=True)
    email = models.EmailField(unique=True, verbose_name='อีเมล')
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
    )

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # ชี้ไปที่ CustomUser
        on_delete=models.CASCADE,
        related_name='profile'
    )
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'
