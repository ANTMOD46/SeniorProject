from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=100, verbose_name='ชื่อ')
    last_name = models.CharField(max_length=100, verbose_name='นามสกุล')
    address = models.TextField(verbose_name='ที่อยู่')
    phone_number = models.CharField(max_length=15, verbose_name='เบอร์โทรศัพท์')
    email = models.EmailField(unique=True, verbose_name='อีเมล')
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    
    # Specify related names to avoid clashes with default User model
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Change to avoid collision
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Change to avoid collision
        blank=True,
    )

    def __str__(self):
        return self.username
