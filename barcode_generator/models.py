from django.db import models

class GeneratedBarcode(models.Model):
    code = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='media/barcodes/')

    def __str__(self):
        return self.code
