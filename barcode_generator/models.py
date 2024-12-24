from django.db import models
import os
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.conf import settings

class GeneratedBarcode(models.Model):
    code = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='media/barcodes/')

    def __str__(self):
        return self.code



@receiver(pre_delete, sender=GeneratedBarcode)
def move_image_to_barchive(sender, instance, **kwargs):
    if instance.image:
        old_path = instance.image.path
        barchive_dir = os.path.join(settings.MEDIA_ROOT, 'barchive')
        if not os.path.exists(barchive_dir):
            os.makedirs(barchive_dir)
        new_path = os.path.join(barchive_dir, f'deleted_{os.path.basename(old_path)}')
        os.rename(old_path, new_path)
